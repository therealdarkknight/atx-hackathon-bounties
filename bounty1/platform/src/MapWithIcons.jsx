import { motion } from "framer-motion";
import { Box, Text, Heading, List } from "@chakra-ui/react";
import { MdCheckCircle } from "react-icons/md";
import { ChevronDown } from "lucide-react";
import React, { useEffect, useState, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import Timeline from "./Timeline";
import { LuCheck, LuPackage, LuShip } from "react-icons/lu";
import '../public/truck.png'

// Timeline events:
// 
// - (Spawn ) Border control conversation w/ icon (T)
// - (Spawn single event) Voice agent + Video check in

mapboxgl.accessToken = "pk.eyJ1IjoiYWxlaW5pbiIsImEiOiJjbTdwd2Z3ZXIwcW5oMmlvam45dTcyMnI3In0.DkbPYr0zytzsrdPJbnupNQ";

const items = [
  {
    title: "Cargo Loading",
    description: "6:18 AM - 13th February 2025",
    texts: [
      "Something about cargo loaded",
    ],
    icon: LuPackage,
  },
  {
    title: "Order In-Progress",
    description: "7:42 AM",
    icon: LuPackage,
  },
  {
    title: "Customs Check",
    description: "8:10 AM",
    texts: [
        "Delayed! Driver reported additional inspection.",
        "New ETA +1hr"
    ],
    icon: LuPackage,
  },
  {
    title: "Speeding Check-In",
    description: "9:32 AM",
    texts: [
        "Driver acknowledges that everythings ok."
    ],
    icon: LuPackage,
  },
  {
    title: "Connectivity Lost",
    description: "10:07 AM",
    icon: LuPackage,
  },
  {
    title: "Stop Detected",
    description: "10:29 AM",
    icon: LuPackage,
  },
  {
    title: "Possible cooling issue.",
    description: "10:42 AM",
    texts: [
        "Driver reported strange noise coming from rear."
    ],
    icon: LuPackage,
  },
  {
    title: "Truck began moving.",
    description: "11:01 AM",
    texts: [
        "New ETA +1:30",
    ],
    icon: LuPackage,
  },
];

const trucks = [
  { 
    id: 1, 
    lat: 25.6866, 
    lng: -100.3161, 
    status: 'loading', 
    name: 'Truck' 
  },
  { 
    id: 2, 
    lat: 25.9164, 
    lng: -100.229, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 3, 
    lat: 26.0473, 
    lng: -100.1868, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 4, 
    lat: 26.216, 
    lng: -100.100, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 5, 
    lat: 26.4072, 
    lng: -100.054, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 6, 
    lat: 26.5741, 
    lng: -99.9777, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 7, 
    lat: 26.7082, 
    lng: -99.90846, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 8, 
    lat: 26.9371, 
    lng: -99.7914, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 9, 
    lat: 27.1518, 
    lng: -99.677, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 10, 
    lat: 27.3327, 
    lng: -99.58099, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 11, 
    lat: 27.4996, 
    lng: -99.50258, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 12, 
    lat: 27.8322, 
    lng: -99.41030, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 13, 
    lat: 28.3949, 
    lng: -99.2594, 
    status: 'moving', 
    name: 'Truck' 
  },
  { 
    id: 14, 
    lat: 28.5732, 
    lng: -99.1988, 
    status: 'moving', 
    name: 'Truck' 
  },
];

const truckList = [
    {
        id: 1,
        name: "Fastly",
        eta: [
            "On Time",
            "+2",
            "+1",
            "+1:30",
            "+0:50",
        ]
    },
    {
        id: 2,
        name: "Amazon",
        eta: [
            "-1:00",
            "-1:20",
            "-0:30",
            "On Time",
            "+0:20",
        ]
    },
    {
        id: 3,
        name: "Express",
        eta: [
            "+1:00",
            "+1:45",
            "+2:35",
            "+3:15",
            "Detention",
        ]
    },
    {
        id: 4,
        name: "Alibaba",
        eta: [
            "On Time",
            "-0:20",
            "-0:45",
            "-0:15",
            "On Time",
        ]
    }
]
  
const statusIcons = {
  moving: 'truck.png',
  stopped: 'https://cdn-icons-png.flaticon.com/512/1828/1828884.png',
  maintenance: 'https://cdn-icons-png.flaticon.com/512/3523/3523883.png',
  loading: 'https://cdn-icons-png.flaticon.com/512/3523/3523883.png',
};

const MapWithIcons = () => {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const [selectedTruck, setSelectedTruck] = useState(null);

  // Controls the right sidebar open/close
  const [isOpen, setIsOpen] = useState(true);
  const [currentLevel, setCurrentLevel] = useState(0);

  // When a truck is clicked from the list:
  const handleTruckClick = (truckId) => {
    setSelectedTruck(truckId);
    setIsOpen(true);
  };

  let list = [1, 10, 11, 12, 13, 14]

  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === 'ArrowRight') {
        setCurrentLevel((prevLevel) => prevLevel + 1);
      }
    }

    window.addEventListener('keydown', handleKeyDown);

    // Cleanup the event listener on unmount
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);
  console.log(currentLevel)

  useEffect(() => {
    if (mapRef.current) return; // Prevent reinitializing the map

    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-99.207, 26.641],
      zoom: 7,
    });

    mapRef.current.addControl(new mapboxgl.NavigationControl(), 'bottom-left');
    mapRef.current.addControl(new mapboxgl.FullscreenControl(), 'bottom-left');
    }, []);
    
  const markersRef = useRef([]); // Store references to created markers

  useEffect(() => {
    // Remove previous markers before rendering new ones
    markersRef.current.forEach(marker => marker.remove());
    markersRef.current = []; // Clear stored markers

    const displayedTrucks = trucks.slice(0, list[currentLevel]);

    displayedTrucks.forEach((truck, index) => {
      const markerEl = document.createElement('div');
      markerEl.style.backgroundImage = `url(truck.png)`;
      markerEl.style.backgroundSize = 'cover';
      markerEl.style.width = '30px';
      markerEl.style.height = '30px';
      markerEl.style.cursor = 'pointer';
      markerEl.style.opacity = (index == (list[currentLevel] - 1) ? '1.0' : '0.6');

      const marker = new mapboxgl.Marker(markerEl)
        .setLngLat([truck.lng, truck.lat])
        .setPopup(
          new mapboxgl.Popup().setHTML(`<h4>${truck.name}</h4><p>Status: ${truck.id}</p>`)
        )
        .addTo(mapRef.current);

      markersRef.current.push(marker);

      // Highlight truck in the list when clicking the marker
      markerEl.addEventListener('click', () => {
        setSelectedTruck(truck.id);
        setIsOpen(true);
      });

      return () => {
        markersRef.current.forEach(marker => marker.remove());
        markersRef.current = [];
      };
    });
  }, [currentLevel]);

    // const directions = new MapboxDirections({
    //     accessToken: mapboxgl.accessToken,
    //     unit: 'metric',
    //     profile: 'mapbox/driving'
    // });
    // mapRef.current.addControl(directions, 'bottom-left');
    // directions.setOrigin([-100.255, 25.6597]);
    // directions.setDestination([-98.0650, 29.735]);

  // Find the currently selected truck details, if any
  const currentTruck = trucks.find((t) => t.id === selectedTruck);

  return (
    <Box>
      {/* Sidebar List (left) */}
      <div className="truck-list">
        <h3>Truck Status</h3>
        <ul>
          {truckList.map((truckList, index) => (
            <li
              key={truckList.id}
              className={index == 0 ? 'selected' : ''}
            >
              <img src={"truck.png"} className="icon" />
              {truckList.name}: {truckList.eta[currentLevel]}
            </li>
          ))}
        </ul>
      </div>

      {/* Map Container */}
      <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>
        <div ref={mapContainerRef} className="map-container" />
      </div>

      {/* RIGHT SIDEBAR */}
      <Box className={`right-sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h3>Truck Details</h3>
          {/* Collapse/expand button */}
          <button 
            className="close-btn" 
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Toggle sidebar"
          >
            <ChevronDown 
              style={{
                transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.3s',
              }}
            />
          </button>
        </div>

        {/* Sidebar content based on selected truck */}
        <Timeline items={items} />
      </Box>
    </Box>
  );
};

export default MapWithIcons;
