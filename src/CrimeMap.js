import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const CrimeMap = ({ dataUrl }) => {
    const [crimes, setCrimes] = useState([]);

    useEffect(() => {
        fetch(dataUrl)
            .then(res => res.json())
            .then(data => setCrimes(data))
            .catch(err => console.error("Failed to load crime data:", err));
    }, [dataUrl]);

    const fallbackCoordinates = [42.447, -76.484]; // Default to Cornell campus

    return (
        <MapContainer center={fallbackCoordinates} zoom={16} style={{ height: '600px', width: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

            {crimes.map((crime, idx) => {
                // You will geocode properly later. For now: fallback to center
                const position = fallbackCoordinates;

                return (
                    <Marker key={idx} position={position}>
                        <Popup>
                            <strong>{crime.incidentType}</strong><br />
                            <em>{crime.location}</em><br />
                            {crime.reported}<br />
                            <small>{crime.disposition}</small><br />
                            <p>{crime.narrative}</p>
                        </Popup>
                    </Marker>
                );
            })}
        </MapContainer>
    );
};

export default CrimeMap;
