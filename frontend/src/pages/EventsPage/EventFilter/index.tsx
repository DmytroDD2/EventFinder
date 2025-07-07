
import styles from "./index.module.css"

import { FaChevronUp, FaChevronDown } from 'react-icons/fa';
import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import {useSearchParams } from 'react-router-dom';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import Slider from 'react-range-slider-input';
import 'react-range-slider-input/dist/style.css';
import "./slyder_styles.css";
import {motion, AnimatePresence} from 'framer-motion'
import clsx from "clsx";
import CategorySelect from "@/components/CategorySelect";
import { Category } from "@/types/event";
import Button from "@/components/Button";






type FormData  ={
    location: string;
    category: string;
    search_term: string;
}


const options: Array<{value: Category, label: Category}> = [
    { value: 'Music', label: 'Music' },
    { value: 'Sport', label: 'Sport' },
    { value: 'Arts', label: 'Arts' },
    { value: 'Technology', label: 'Technology' },
    {value: 'Other', label: 'Other' },
  ];



const EventFilter: React.FC<{ dark: boolean }> = ({ dark }) => {
    const [searchParams,setSearchParams] = useSearchParams();
    const [isCollapsed, setIsCollapsed] = useState(true); 
    const { register, handleSubmit } = useForm<FormData>({
        defaultValues: {
          search_term: searchParams.get('search_term') ?? '',
          location: searchParams.get('location') ?? '',
        },
      });;


    const [startDate, setStartDate] = useState<Date | null>(
    searchParams.get('start_date') ? new Date(searchParams.get('start_date')!) : null
    );

    const [endDate, setEndDate] = useState<Date | null>(
    searchParams.get('end_date') ? new Date(searchParams.get('end_date')!) : null
    );

    const [minPrice, setMinPrice] = useState<number>(
    searchParams.get('min_price') ? Number(searchParams.get('min_price')) : 0
    );

    const [maxPrice, setMaxPrice] = useState<number>(
    searchParams.get('max_price') ? Number(searchParams.get('max_price')) : 0
    );

    const [category, setCategory] = useState<Category | null>(
    (searchParams.get('category') as Category) ?? null
    );


    const onSubmit: SubmitHandler<FormData> = (data) => {
        const queryParams = new URLSearchParams();

        if (startDate) queryParams.append('start_date', startDate.toISOString().split('T')[0]);
        if (endDate) queryParams.append('end_date', endDate.toISOString().split('T')[0]);
        if (data.location) queryParams.append('location', data.location);
        if (category) queryParams.append('category', category);
        if (data.search_term) queryParams.append('search_term', data.search_term);
        if (minPrice) queryParams.append('min_price', minPrice.toString());
        if (maxPrice) queryParams.append('max_price', maxPrice.toString());

        queryParams.append('page', '1');
        queryParams.append('per_page', '10');

        setSearchParams(queryParams);
    };
 
    
    const toggleCollapse = () => {
        setIsCollapsed(!isCollapsed);
    };
    
 
    return (
        <form 
          onSubmit={handleSubmit(onSubmit)}
          className={clsx(styles.formContainer,
            {[styles.dark_form]: dark}
        )}
          >
            <AnimatePresence>
                {!isCollapsed &&
                
                        <motion.div
                        initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                            exit={{ opacity: 0, height: 0 }}
                            transition={{ duration: 0.2 }}
                            className={styles.formContainer}
                        key={location.pathname}
             
                        >
                            <input className={styles.input_search} type="text" {...register('search_term')} placeholder="Search Term" />
                            <div>
                                <DatePicker
                                    selected={startDate}
                                    onChange={(date) => setStartDate(date)}
                                    dateFormat="yyyy/MM/dd"
                                    placeholderText={"Start"}
                                    className={styles.datePicker}
                                />
                            </div>
                            <div>
                                <DatePicker
                                    selected={endDate && endDate}
                                    onChange={(date) => setEndDate(date)}
                                    dateFormat="yyyy/MM/dd"
                                    placeholderText="End"
                                    className={styles.datePicker}
                                />
                            </div>
                            <input className={styles.input_location} type="text" {...register('location')} placeholder="Location" />
                            <CategorySelect
                                 options={options}
                                 setCategory={setCategory}
                                 className={styles.input_category}
                                 {...category && {defaultValue: category}}
                                  />
                
                            <div className={styles.slider_container}>
                                <p>Price</p>
                                <Slider
                                    min={0}
                                    max={10000}
                                    value={[minPrice, maxPrice]}
                                    // id={styles.slider}
                                    id={clsx(!dark ?"range-slider-gradient" :"dark-slider")}
                                    className="margin-lg"
                                    onInput={(value) => {
                                        setMinPrice(value[0]);
                                        setMaxPrice(value[1]);
                                    }}
                                />
                
                                <p>{`${minPrice} - ${maxPrice} ₴`}</p>
                
                            </div>
                
                            <Button
                                   className={styles.button_submit}
                                   type="submit"
                                //    onClick={() => handleClick(event)}
                                   whileHover={{backgroundColor: "#ee8aab"}}
                                   whileTap={{ scale: 0.95 }}
                                   transition={{ duration: 0.2 }}
                                  >
                                    Search
                            </Button>
                        </motion.div>
                   
                }
            </AnimatePresence>
            <button 
                onClick={toggleCollapse}
                className={clsx(styles.toggleButton, { [styles.dark_toggle]: dark })}
            >
                {isCollapsed ? <FaChevronUp className={styles.icon}/> : <FaChevronDown className={styles.icon} />}
            </button>
        
        
        </form>
    );
};

export default EventFilter;

