import React from 'react'
import styles from "./index.module.css"

import DefaultImage from '@/assets/icons/default_image.png'
import { ImageType } from '@/types/image';
import * as motion from "motion/react-client"


const ImageEvent = ({images}: {images: (ImageType | null)[]}) => {
  const [image, setImage] = React.useState<string>( images[0]?.image_url || DefaultImage);

  
  return (
    <section className={styles.container}>
      <img src={image} />
      {images[0] && 
        <div className={styles.images_list}>
          {images.map((img, index) => (
            <motion.img 
            key={index} 
            src={img?.image_url || DefaultImage} 
            className={styles.image}
            onClick={() => setImage(img?.image_url || DefaultImage)} 
            

            // whileHover={{ scale: 1.05 }} 
            whileTap={{ scale: 0.95 }}  
            
            transition={{ duration: 0.2 }} 
          />
          ))}
        </div>}
        
    </section>

    
  )
}

export default ImageEvent