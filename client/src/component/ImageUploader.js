
import React from "react";
import { useState } from "react";
import '../style/ImageUploader.css';
import OutputAlgoritm from "./OutputAlgoritm";
export default function FileUploader({ type }) {
    const [image, setImage] = useState(null);
    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function () {
                setImage(reader.result);
            }
            reader.readAsDataURL(file);
        } else {
            setImage(null);
        }
    };
    return (
        <div >

            <div className="upload-container">
                <div className="upload-preview" style={{ border: image ? 'none' : '3px dashed #ccc' }}>
                    {image ?
                        type == "video" ?
                            <video autoPlay="true" controls src={image} alt="תמונה" style={{ maxWidth: '2000%', maxHeight: '500px', display: 'inline', margin: '0 auto 100px' }} />
                            : <img src={image} alt="תמונה" style={{ maxWidth: '100%', maxHeight: '500px', display: 'block', margin: '0 auto 20px' }} />

                        : <div id="previewText">אנא בחר {type == "video" ? "סירטון" : "תמונה"} להעלאה</div>}
                </div>

                {
                    type == "video" ?
                        <input type="file" id="uploadFile"  accept= "video/*" className="upload-input" onChange={handleImageUpload} />
                        :

                        <input type="file" id="uploadFile" accept= "image/*"  className="upload-input" onChange={handleImageUpload} />
                }
                <label htmlFor="uploadFile" className="upload-label">בחר {type == "video" ? "סירטון" : "תמונה"}</label>
            </div>
            {image?
            <OutputAlgoritm />
            : null
            }
        </div>
    );
};

// export default ImageUploader;

