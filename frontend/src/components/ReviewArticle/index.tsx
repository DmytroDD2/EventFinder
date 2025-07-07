import { TypeUserReview } from "@/types/reviews";
import styles from "./index.module.css"
import DefaultImage from '@/assets/icons/default_image.png';
import StarRating from "../StarRating";
import { useRef, useState } from "react";
import clsx from "clsx";
import { useNavigate, useLocation } from "react-router-dom";
import Button from "../Button";
import useDeleteReviews from "@/hooks/reviews/useDeleteReviews";
import {AnimatePresence, motion} from "framer-motion"

type ReviewArticleProps ={
  reviews: TypeUserReview[],
  dark: boolean, 
  scroll?: boolean,
} 

const ReviewArticle = ({ reviews, dark, scroll=false}: ReviewArticleProps) => {
  const [expandedItems, setExpandedItems] = useState<Record<string, boolean>>({});
  const itemRefs = useRef<Record<number, HTMLDivElement | null>>({});
  const navigate = useNavigate();
  const location = useLocation();
  
  const deleteButton = 
      location.pathname.includes('admin') || 
      location.pathname.includes('reviews')
      ? true
      : false

  const {deleteReview} = useDeleteReviews()

  const navigateToEvent = () => {
    navigate(`/events/${reviews[0].event_id}`);
  }

  const toggleExpanded = (id: number) => {
    
    setExpandedItems(prev => ({
      ...prev,
      [id]: !prev[id],
    }));
    
     itemRefs.current[id]?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };


  return reviews.length > 0 ? (
    <section className={clsx(
      styles.reviewArticle, dark && styles.dark,
      scroll && styles.scroll
      )}>

      <AnimatePresence>
        {reviews.map((review) => {
          const isExpanded = expandedItems[review.id] || false;
          return (
            <motion.article
        
              initial={{ scale: 1, opacity: 1 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0, opacity: 0 }}
              // exit={{ x: '-100%', opacity: 0 }}
              transition={{ duration: 0.4 }}
              key={review.id}
              ref={(el: HTMLDivElement | null) => {
                  itemRefs.current[review.id] = el;
              }}
              id={`review-${review.id}`}
              onClick={navigateToEvent}
              className={clsx(
                styles.reviewItem,
                isExpanded && styles.expandedItem
              )}
            >  
            {deleteButton &&
            
                <Button
                    className={styles.removeButton}
                    aria-label="Remove image"
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteReview(review.id)
                      }}
                  >
                    ✕
                </Button>
            }

              <div className={styles.rating}>
                <p>Rating:</p>
                <StarRating rating={review.rating} />
              </div>
              <p className={`${styles.description} ${isExpanded ? styles.expanded : ''}`}>
                {review.description}
              </p>
              {review.description.length > 100 && (
                <button
                  className={styles.toggleButton}
                  onClick={(e) => {
        
                    toggleExpanded(review.id);
                    e.stopPropagation();
        
                  }}
                >
                  {isExpanded ? 'Collapse' : 'Read more'}
                </button>
              )}
              <div className={styles.footer_container}>
                <img
                  src={review.image_url || DefaultImage}
                  alt={review.name || 'User image'}
                  className={styles.img}
                />
                <h3 className={styles.name}>
                  {review.name}
                </h3>
              </div>
            </motion.article>
          );
        })}
      </AnimatePresence>
    </section>
  ) : (
    <p>No reviews available.</p>
  );
};


export default ReviewArticle