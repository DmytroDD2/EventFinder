
import StarRating from '../StarRating';
import styles from './index.module.css';
import Button from '../Button';
import clsx from 'clsx';
import { useParams } from 'react-router-dom';
import useCreateReview from '@/hooks/reviews/useCreateReview';
import { useState } from 'react';




const CreateReview = ({ dark }: { dark: boolean }) => {
    const { eventId } = useParams();
    const [rating, setRating] = useState<number>(0);
    const [description, setDescription] = useState<string>('');
    const { createReview, isCreating, createError } = useCreateReview();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!eventId) return;
        
        try {
            await createReview({ 
                eventId, 
                rating, 
                description 
            });
           
            setRating(0);
            setDescription('');
        } catch (error) {
            console.error('Failed to submit review:', error);
        }
    };

    return (
        <div className={clsx(styles.container, dark && styles.dark)}>
            <h1 className={styles.title}>Leave a Review</h1>

            {createError && (
                <div className={styles.error}>
                    {createError instanceof Error ? createError.message : 'Failed to submit review'}
                </div>
            )}

            <form onSubmit={handleSubmit} className={styles.form}>
                <div className={styles.divider}></div>

                <div className={styles.section}>
                    <h2 className={styles.sectionTitle}>Your Rating</h2>
                    <StarRating 
                        rating={rating} 
                        starSize="1.5rem"
                        onRatingChange={setRating} 
                    />
                </div>

                <div className={styles.section}>
                    <h2 className={styles.sectionTitle}>Your Review</h2>
                    <p className={styles.description}>Share your impressions about the store</p>
                    <textarea
                        className={styles.textarea}
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="Write your review here..."
                        required
                    ></textarea>
                </div>

                <div className={styles.buttonContainer}>
                    <Button 
                        type="submit" 
                        className={styles.submitButton}
                        disabled={isCreating}
                    >
                        {isCreating ? 'Submitting...' : 'Опублікувати відгук'}
                    </Button>
                </div>
            </form>
        </div>
    );
};

export default CreateReview;