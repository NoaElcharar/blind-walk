import { useState } from "react";

export default function OutputAlgoritm(){


    const [outputText, setOutputText] = new useState("המשך ישר");


    return <div>
        <h1>{outputText}</h1>
    </div>

}