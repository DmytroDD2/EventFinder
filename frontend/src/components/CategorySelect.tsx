

import { Category } from '../types/event';
// import styles from './YourStyles.module.css';
// import categoryImage from  '../assets/category.png';
import { useRef, useState } from 'react';
import clsx from 'clsx';
import * as motion from "motion/react-client"
import { useOnClickOutside } from 'usehooks-ts'


const CategorySelect = (
   {options, setCategory, className, defaultValue}: {
    options: Array<{ value: Category; label: Category}>;
    setCategory: (value: Category) => void;
    className?: string;
    defaultValue?: Category 
   }
   ) =>
 {
  const defaultOption = options.find(option => option.value === defaultValue) || options[0];
  
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(defaultOption || options[0]);


  
 
  const selectRef = useRef<HTMLDivElement>(null!); 

  useOnClickOutside(selectRef, () => setIsOpen(false)); 
  return (

    <div className={clsx("custom-select-container", className, { open: isOpen  })} ref={selectRef}>
      <div 
        className="selected" 
        onClick={() => setIsOpen(!isOpen)}>
        {selected.label}
        <svg
          className="arrow-down"
          width="4"
          height="5"
          viewBox="0 0 20 24"
          fill="none"
          stroke="black"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </div>
      {isOpen && (
        <motion.ul
          className="custom-options"
          initial={{ opacity: 0, scaleY: 0 }}
          animate={{ opacity: 1, scaleY: 1 }}
          exit={{ opacity: 0, scaleY: 0 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          style={{ transformOrigin: "top" }}
        >
          {options.map(option => (
            <li 
              
              key={option.value}
              className={selected.value === option.value ? 'selected-option' : ''}
              onClick={() => {
                setSelected(option);
                setIsOpen(false);
                setCategory(option.value);
              }}
            >
              {option.label}
            </li>
          ))}
        </motion.ul>
      )}
    </div>
  );
}

export default CategorySelect;