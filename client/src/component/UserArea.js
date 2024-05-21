import { Link, Routes, Route, Outlet } from "react-router-dom"
import '../style/Login.css'
import FileUploader from "./ImageUploader"
import OutputAlgoritm from "./OutputAlgoritm"
export default function UserArea() {

    return (
        <div >
            <h2>hello {sessionStorage.getItem('user')}</h2>

            
            <Link to={"address"} >הכנס כתובת אליה תרצה להגיע</Link>
            <div className="up">
            <FileUploader type={"video"} />
            <FileUploader type={"image"} />
            <OutputAlgoritm />

            </div>
            {/* <div className="bar">
                <Link to="./uploadImage"> upload image </Link>
                <Link to="./uploadVideo"> upload video </Link>
            </div>
            <div className="body"> 

                <Outlet />

            </div> */}

        </div>

    )
}
