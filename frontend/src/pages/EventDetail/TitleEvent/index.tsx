import React from 'react'
import styles from "./index.module.css"
import Point from '@/assets/icons/point.png';
import Calendar from '@/assets/icons/calendar.png';
import clsx from 'clsx';
import { transformDate } from '@/utils/data_format';

interface TitleEventProps {
  vanue: string | null;
  date: string | null;
  name: string;
  dark: boolean;
}

const TitleEvent = ({ vanue, date, name, dark}: TitleEventProps) => {
  return (
    <section className={styles.container}>
        <h1 className={clsx(dark && styles.dark)}>{name}</h1>
        <div className={styles.info}>
            <div>
                <img src={Calendar}></img>
                <p className={styles.pink_font}>
                  {date ? 
                    transformDate(date) : "still unknown"}
                </p>
            </div>
            <div>
                <img src={Point}></img>
                <p>{vanue}</p>
            </div>
        </div>
    </section>
  )
}

export default TitleEvent