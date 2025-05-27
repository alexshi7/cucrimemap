import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const CrimeMap = ({ dataUrl }) => {
    const [crimes, setCrimes] = useState([]);
    const [locationMap, setLocationMap] = useState({});
    const fallbackCoordinates = [42.447, -76.484]; // Default to Cornell campus

    // Load crimes
    useEffect(() => {
        fetch(dataUrl)
            .then(res => res.json())
            .then(data => setCrimes(data))
            .catch(err => console.error("Failed to load crime data:", err));
    }, [dataUrl]);

    // Load location map
    useEffect(() => {
        fetch('/location-map.json')
            .then(res => res.json())
            .then(data => setLocationMap(data))
            .catch(err => console.error("Failed to load location map:", err));
    }, []);

    // Helper to get coordinates for a location string
    const getCoordinates = (location) => {
        if (!locationMap || !location) return fallbackCoordinates;
        // Try exact match
        if (locationMap[location]) {
            return [locationMap[location].lat, locationMap[location].lng];
        }
        // Try partial match (for locations like "Barton Hall Bike Rack")
        const key = Object.keys(locationMap).find(k => location.includes(k));
        if (key) {
            return [locationMap[key].lat, locationMap[key].lng];
        }
        return fallbackCoordinates;
    };

    return (
        <MapContainer center={fallbackCoordinates} zoom={16} style={{ height: '600px', width: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

            {crimes.map((crime, idx) => {
                const position = getCoordinates(crime.location);

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