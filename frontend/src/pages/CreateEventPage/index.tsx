
import clsx from 'clsx';
import {useForm, SubmitHandler} from 'react-hook-form';
import styles from './index.module.css';
import { useEffect, useRef, useState } from 'react';
import DatePicker from 'react-datepicker';
import CategorySelect from '@/components/CategorySelect';
import Button from '@/components/Button';
import { optionsCategory } from '@/utils/events';
import ImageUpload from '@/components/DropezoneFile';
import { useThemeStore } from '@/store/themeStore';
import { useCreateEvent } from '@/hooks/events/useCreateEvent';
import { Category} from '@/types/event';
import { useNavigate, useParams } from 'react-router-dom';
import { yupResolver } from '@hookform/resolvers/yup';
import { eventSchema } from '@/utils/validation';

import { useUpdateTextEvent } from '@/hooks/events/useUpdeteTextEvent';
import { useEventDetail } from '@/hooks/events/useEventDetail';
import { ImageType } from '@/types/image';
import { useAddEventImages } from '@/hooks/events/useEventAddImages';







export type EventFormType = {
  name: string;
  description: string;
  total_tickets: number;
  venue: string;
  price?: number;
  category?: Category;
  images?: (ImageType | string | Blob)[];
  data?: string;
};

type EventFormProps = {

  isEditMode?: boolean;
};

export const CreateEventPage = ({ isEditMode = false }: EventFormProps) => {
    const {
         register,
         reset, 
         handleSubmit,
         setValue,
         getValues,
         formState: { errors }
    }= useForm<EventFormType>({ resolver: yupResolver(eventSchema), mode: "onChange"})
    
    const { eventId, userId } = useParams();
    
    const {event} =  useEventDetail(eventId);
    const [Eventdate, setEventdate] = useState<Date | null>(null);

    const [category, setCategory] = useState<Category>("Other");
    const initialized = useRef(true);
    
    const {theme} = useThemeStore();
    const check_dark = theme === 'dark'
    
    const {createEvent} = useCreateEvent(userId);
    const { updateText } = useUpdateTextEvent();
    const {addImages} = useAddEventImages()
    const navigate = useNavigate();


    useEffect(() => {

        if (isEditMode && event && !initialized.current) {
            reset({
                name: event.name,
                description: event.description,
                total_tickets: event.total_tickets,
                venue: event.venue,
                price: event.price,
                images: event.images ? event.images.filter((img) => img !== null) : [],
            });
            setCategory(event.category);
            setEventdate(event.data ? new Date(event.data) : null);
            initialized.current = true;
        }

        return () => {initialized.current = false;};
        },
        [isEditMode, event, reset]);


    const onSubmit: SubmitHandler<EventFormType> = (data: EventFormType) => {
       
        if (Eventdate) data.data = Eventdate.toISOString();
        data.category = category
        if (isEditMode && eventId) {
            
            if (event) {
                // addImages({ eventId, images: data.images });
                if (data?.images && eventId) {
                    const files = data.images.filter((img): img is File => img instanceof File || img instanceof Blob)
                        .map(img => img instanceof File ? img : new File([img], "image.jpg"));
                    addImages({ eventId, images: files });
                }
                updateText({ id: eventId, data, event }).then(() => {
                    navigate(
                        userId 
                        ? `/admin/${userId}/events` 
                         :'/events', { replace: true })
                });
            }
        } else {
            createEvent(data).then(() => {
                navigate(
                    userId 
                        ? `/admin/${userId}/events` 
                         :'/events', { replace: true });
            });
        }
        
    };

    const onCacnel = () => {
        reset();
        setCategory("Other");
        setEventdate(null);
    }

    return (
        <div className={styles.container}>
            <form 
            
                onSubmit={handleSubmit(onSubmit)}
                className={clsx(styles.form_container, { [styles.dark_form]: check_dark })}
            >
                <h1 className={styles.title}>{isEditMode ? 'Edit Event' : 'Create Event'}</h1>
                <p className={styles.description}>Fill in the event information</p>

                <div className={styles.input_grup}>
                    <label htmlFor="event_name"> Event Name</label>
                    <input
                        type="text"
                        {...register('name')}
                        placeholder="Enter event name"
                    />
                     <p className={styles.error}>{errors.name?.message as string}</p>
                </div>
                
                <div className={styles.input_grup}>
                    <label >Category</label>
                    <CategorySelect
                        options={optionsCategory}
                        setCategory={setCategory}
                        className={styles.input_category}
                        // {...(category && { defaultValue: category })}
                    />
                </div>

                <div className={styles.input_grup}>
                    <label htmlFor="location">Location</label>
                    <input
                     type="text" {...register('venue')}
                     placeholder="Enter event location" />
                    <p className={styles.error}>{errors.venue?.message as string}</p>
                </div>

                <div className={styles.input_grup}>
                    <label htmlFor="description">Event Description</label>
                    <textarea
                        className={styles.textarea_description}
                        {...register('description')}
                        placeholder="Enter event description">

                    </textarea>
                
                </div>


         
                <div className={styles.input_tickets_price}>
                    <div className={styles.input_grup}>
                        <label htmlFor="price">Tickets Price</label>
                         <input
                            className={styles.input_price}
                            type="number"
                            {...register('price')}
                            placeholder="Enter event price"
                        />
                    </div>
                    
                    <div className={styles.input_grup}>
                        <label htmlFor="total_tickets">Number of Tickets</label>
                        <input
                            className={styles.input_tickets}
                            type="number"
                            {...register('total_tickets')}
                            placeholder="Enter total tickets"
                        />
                        <p className={styles.error}>{errors.total_tickets?.message as string}</p>
                    </div>

                </div>
          

                <div className={styles.input_grup}>
                    <label htmlFor='even_tdate'>Data</label>
                    <DatePicker
                        selected={Eventdate}
                        onChange={(date) => setEventdate(date)}
                        dateFormat="yyyy/MM/dd"
                        placeholderText="Data"
                        className={styles.datePicker}
                        name='even_tdate'
                    />
                    {/* <p className={styles.error}>{errors.data?.message as string}</p> */}
                </div>
                
                <div className={styles.input_grup}>
                    <label>Event Images</label>
                    <ImageUpload
                     register={register}
                     getValues={getValues}
                     setValue={setValue}
                     dark={check_dark}
                     editImages={event?.images}
                    />
                </div>
                
                <div className={styles.button_container}>
                    <Button
                        className={styles.button_cancel}
                        onClick={onCacnel}
                    >
                        Cancel
                    </Button>
                    <Button
                        className={styles.button_submit}
                        type="submit"
                    >
                    {isEditMode ? 'Update Event' : 'Create Event'}
                    </Button>
                </div>
            </form>
        </div>
    );
};

export default CreateEventPage;