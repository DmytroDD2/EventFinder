import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import styles from './index.module.css';
import {UseFormGetValues, UseFormRegister, UseFormSetValue } from 'react-hook-form';
import Frame from '@/assets/icons_svg/frame.svg?react';
import Button from '../Button';
import {AnimatePresence, motion} from 'framer-motion';
import clsx from 'clsx';

import { EventFormType } from '@/pages/CreateEventPage';
import { ImageType } from '@/types/image';
import { useDeleteImage } from '@/hooks/events/useDeleteImage';



type TypeImageUpload = {
  register: UseFormRegister<EventFormType>;
  setValue: UseFormSetValue<EventFormType>;
  getValues: UseFormGetValues<EventFormType>;
  name?: "images"
  dark?: boolean;
  editImages?: ImageType[] | undefined;
};




const ImageUpload = ({ setValue, getValues,dark, name = 'images', editImages }: TypeImageUpload) => {
  const [previews, setPreviews] = useState<(File & { preview: string })[]>([]);
  const {deleteImage} = useDeleteImage()

  const handleDeleteOnbackand = (eventId: string | number, imageId: string | number) => {
    deleteImage({eventId, imageId});
  }


  const onDrop = useCallback((acceptedFiles: File[]) => {
   
    setValue(name, [...(getValues(name) || []), ...acceptedFiles]);
    const previewUrls = acceptedFiles.map(file =>
      Object.assign(file, {
        preview: URL.createObjectURL(file),
      })
    );
    setPreviews(prevPreviews => prevPreviews.concat(previewUrls)); 
  }, [setValue, name, getValues]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: true,
    accept: {
      'image/*': []
    }
  });
  
  const removeImage = (index: number) => {
    const updatedImages = [...(getValues(name) || [])];
    updatedImages.splice(index, 1);
    setValue(name, updatedImages);
    setPreviews(previews.filter((_, i) => i !== index));
  }
  return (
    <div className={clsx(styles.uploadWrapper, dark && styles.dark)}>
      {/* <label className={styles.label}>Drag or drop images</label> */}

      <div {...getRootProps({ className: styles.dropzone })}>
        <input {...getInputProps()} />
        <Frame />
        <p>{isDragActive ? 'Drop the files here...' : 'Drag & drop or click to upload images'}</p>
      </div>

      <div className={styles.previewGrid}>
        <AnimatePresence >
          {previews && previews.map((file, idx) => (
            <motion.div
                key={file.preview}
                className={styles.previewItem} 
                initial={{ scale: 0, opacity: 1 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0, opacity: 0 }}
                // exit={{ x: '-100%', opacity: 0 }}
                transition={{ duration: 0.4 }}
            >
        
               <Button
                  type="button"
                  className={styles.removeButton}
                  aria-label="Remove image"
                  onClick={() => removeImage(idx)}
        
                >
                  ✕
               </Button>
              <img
                src={file.preview}
                alt={`preview ${idx}`}
                className={styles.previewImage}
              />
            </motion.div>
          ))}

          {editImages && editImages.length > 0 && editImages.map((image, idx) => (
            
            <motion.div
              key={image.id}
              className={styles.previewItem}
              initial={{ scale: 0, opacity: 1 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0, opacity: 0 }}
              transition={{ duration: 0.4 }}
            >
              <Button
                type="button"
                className={styles.removeButton}
                aria-label="Remove image"
                onClick={() => handleDeleteOnbackand(image.event_id, image.id)}
              >
                ✕
              </Button>
              <img
                src={image.image_url}
                alt={`preview ${idx}`}
                className={styles.previewImage}
              />
            </motion.div>
          ))}

        </AnimatePresence>
      </div>
    </div>
  );
};

export default ImageUpload;
