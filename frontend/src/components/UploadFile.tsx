
import * as motion from "motion/react-client"
import { ReactNode, useRef, useState,} from "react";
import { HTMLMotionProps } from "framer-motion";
import Slider from 'react-range-slider-input';
import clsx from "clsx";
type Props = HTMLMotionProps<'label'> & {
    children: ReactNode
    infoClass?: string
    uploadProgress?: number
    sendImage: (file: File) => void
  };



const UploadFile = ({sendImage, uploadProgress, infoClass, children, ...props}:Props) => {
    const [file, setFile] = useState<File | null>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const image = e.target.files?.[0];
        
        if (image) {
            
            setFile(image);
        }
        

    };

    const sendFile = (e: React.MouseEvent) => {
        
        if (file) {
            e.preventDefault();
            sendImage(file);
            
        }
        setFile(null)
        
        if (inputRef.current) {
            inputRef.current.value = "";
        };
      
    };
  
  return (
    <div>
        <div className={infoClass}>
            {file && file.name}
            {file && uploadProgress !== undefined && uploadProgress > 0 && (
                <Slider
                    min={0}
                    max={100}
                    value={[0, uploadProgress]}
                    disabled
                    id={clsx("range-slider-gradient")} 
                    className="margin-lg"
                />
            )}

        </div>
        <motion.label
            {...props}
            htmlFor="file"
            style={{display: "block "}}
            whileTap={{ scale: 0.95}}  
            transition={{ duration: 0.2 }}
            onClick={sendFile}
         
        > 
          {file ? "accept" :children}
        </motion.label>   
        <input
         name="image"
         id="file"
         type="file"
         style={{display: "none"}}
         onChange={onChange}
         ref={inputRef}
        
         />
    </div>)
}

export default UploadFile

