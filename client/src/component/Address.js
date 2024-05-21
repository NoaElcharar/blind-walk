
// import { useState, useMemo } from "react";
// import { GoogleMap, useLoadScript, Marker } from "@react-google-maps/api";
// import usePlacesAutocomplete, {
// getGeocode,
// getLatLng,
// } from "use-places-autocomplete";
// import {
// Combobox,
// ComboboxInput,
// ComboboxPopover,
// ComboboxList,
// ComboboxOption,
// } from "@reach/combobox";
// import "areach/combobox/styles.css";

// export default function Places() {
// const { isLoaded } = useLoadScript({
// googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY,
// libraries: ["places"],
// });

// if (!isLoaded)return <div>Loading...</div>
// return <Map/>;
// }
// function Map() {
//     const center = useMemo(() => ({ lat: 43.45, lng: -80.49 }), []);
//     const [selected, setSelected] = useState(null);
    
//     return (
//     <>
//     <div className= "places-container">
//     <PlacesAutocomplete setSelected={setSelected} />
//     </div> 
//     <GoogLeMap
//     zoom={10}
//     center={center}
//     mapContainerClassName="map-container"
//     >
//     {selected <Marker position={selected} />}
//     </GoogleMap>
//     </>
//     );
// }
// const PlacesAutocomplete = ({ setSelected }) => {
// const {
// ready,
// value,
// setValue,
// suggestions: { status, data },
// clearSuggestions,
// } = usePlacesAutocomplete();

// const handleSelect = async (address) => {
//     setValue(address, false);
//     clearSuggestions();
    
//     const results =await getGeocode({ address });
//     const {lat, lng} = await getLatLng(results[0]);
//     };
//     return (
//     <Combobox onSelect={handleSelect}>
//     <ComboboxInput
//     value ={value}
//     onChange={(e)=>setValue(e.target.value)}
//     disabled={!ready}
//     className="combobox"
//     placeholder="Search an address"
//     />
//     <ComboboxPopover>
//         <ComboboxList>

// {/* // import React, { useState } from 'react';
// import '../style/Address.css'

// function Address() { */}
// {/* //   const [location, setLocation] = useState('');
//   const [isInside, setIsInside] = useState(false);

//   const handleLocationInput = (event) => { */}
// {/* //     setIsInside(event.target.value === 'inside'); */}
// {/* //   }; */}

// {/* //   const handleAddressInput = (event) => { */}
// {/* //     if (isInside) { */}
// {/* //       // כאן יכולה להיות הלוגיקה להשתמש בכתובת המוזנת
//       console.log('קיבלנו את הכתובת הפנימית:', event.target.value);
    // } else { */}
// {/* //       // כאן יכולה להיות הלוגיקה להשתמש בכתובת החיצונית
//       console.log('קיבלנו את הכתובת החיצונית:', event.target.value);
//     }
//   };

//   return (
//     <div>
//       <label>
//         האם אתה רוצה להשתמש בפנים או בחוץ?
//         <input type="text" onChange={handleLocationInput} />
//       </label>
//       <br />
//       <label>
//         הזן את כתובת היעד:
//         {isInside ? (
//           <input type="text" onChange={handleAddressInput} /> */}
// {/* //         ) : (
//           <span>לא נדרשת כתובת בחוץ</span>
//         )}
//       </label>
//     </div>
//   );
// }

// export default Address; */}
