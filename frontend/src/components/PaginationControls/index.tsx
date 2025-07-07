import { clsx } from 'clsx';

import styles from './index.module.css';
import { useNavigate, useSearchParams } from 'react-router-dom';
import scrollToTopWithOffset from '@/utils/scroll';

interface PaginationControlsProps {
  currentPage?: number;
  totalPages?: number;
  dark?: boolean;
}

const PaginationControls = ({
  currentPage = 1,
  totalPages = 10, 
  dark = false
}: PaginationControlsProps) => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const handlePageChange = (page: number) => {
    const params = new URLSearchParams(searchParams);
    params.set('page', page.toString());
    params.set('per_page', '10'); 
    navigate(`?${params.toString()}`);
    scrollToTopWithOffset('.scroll-wrapper');

  };
  
  return (
    <div className={clsx(styles.pagination, dark && styles.dark)}>
      <button
        onClick={() => handlePageChange(Math.max(1, currentPage - 1))}
        disabled={currentPage === 1}
      >
         &lt; Privious 
      </button>
      
      {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
        <button
          key={page}
          onClick={() => handlePageChange(page)}
          className={clsx(currentPage === page && styles.active)}
        >
          {page}
        </button>
        ))}
      
      <button
        onClick={() => handlePageChange(Math.min(totalPages, currentPage + 1)
      )}
        disabled={currentPage === totalPages}
      >
        Next &gt;
      </button>
    </div>
  );
};

export default PaginationControls;