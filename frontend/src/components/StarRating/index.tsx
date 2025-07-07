import FullStarSvg from '@/assets/icons_svg/estimate_star.svg?react';
import HalfStarSvg from '@/assets/icons_svg/half_star.svg?react';
import EmptyStarSvg from '@/assets/icons_svg/empty_star.svg?react';
import styles from './index.module.css'
import { useState } from 'react';

interface StarRatingProps {
  rating: number;
  starSize?: string;
  className?: string;
  onRatingChange?: (rating: number) => void;
}

function StarRating({ rating, starSize = '1.2rem', className = '', onRatingChange }: StarRatingProps) {
  const stars: React.ReactNode[] = [];
  const normalizedRating = rating / 2;
  const [half, setHalf] = useState(-0.5);

  const handleClick = (index: number) => {
    if (onRatingChange) {
      onRatingChange(index * 2 + half);
      setHalf(prevHalf => -prevHalf);
    }
  };
   

  const pyshrating = (StarComponent: React.FC<React.SVGProps<SVGSVGElement>>, index: number) => {
    stars.push(
    <StarComponent 
      className={`${styles.star} ${styles.clickable}`}
      style={{ height: starSize }} 
      key={index}
      onClick={() => handleClick(index)}
    />
    )
  }
  for (let i = 1; i <= 5; i++) {
    if (normalizedRating >= i) {
      pyshrating(FullStarSvg, i)
    } else if (normalizedRating >= i - 0.5) {
      pyshrating(HalfStarSvg, i)
    } else {
      pyshrating(EmptyStarSvg, i)
    }
  }

  return (
    <div className={`${styles.container} ${className}`}>
      {stars}
    </div>
  );
}

export default StarRating;