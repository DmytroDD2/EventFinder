import useReviews from '@/hooks/reviews/useReviews';
import styles from './index.module.css';
import { useState } from 'react';
import useUserReviews from '@/hooks/reviews/useUserReviews';
import { useParams } from 'react-router-dom';
import ReviewArticle from '@/components/ReviewArticle';
import { useThemeStore } from '@/store/themeStore';
import clsx from 'clsx';
import Button from '@/components/Button';



const ReviewsPage = ({ eventId }: { eventId?: string }) => {
  const [page, setPage] = useState(1);
  const {userId} = useParams()
  const {theme} = useThemeStore();

  const check_dark = theme === 'dark'

  const { reviews, isLoading: reviewsLoading } = useReviews(eventId, page, 10);
  const {userReviews, isLoading: userReviewsLoading} = useUserReviews({ userId, page, perPage: 10, enabled: !eventId });
  
  const isLoading = reviewsLoading || userReviewsLoading;
  const data = eventId ? reviews : userReviews;
  
  const nextPage = data && data.length < 10

  const paginate = (action: 'prev' | 'next') => {
    if (action === 'prev' && page > 1) {
      setPage(page - 1);
    } else if (action === 'next') {
      setPage(page + 1);
    }
  };

  return (
    <div className={clsx(styles.container, check_dark && styles.dark)}>
      {isLoading ? (
        <p>Loading...</p>
      ) :
      <ReviewArticle reviews={data} dark={check_dark} scroll/>
    
      }
      <div className={styles.pagination}>
        <Button
         className={clsx(styles.button, page === 1 && styles.disabled)}
         onClick={() => paginate('prev')}
        >
          Prev
        </Button>
        <Button
         disabled={nextPage}
         className={clsx(
          styles.button,
          nextPage && styles.disabled
        )}
         onClick={() => paginate('next')}
        >
          Next
        </Button>
      </div>
    </div>
  );
};


export default ReviewsPage;