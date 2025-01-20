"use client";
import { useEffect, useRef, useState } from "react";
import Script from "next/script";
import { Spinner } from "@chakra-ui/react";

export default function GoogleMap() {
  const mapRef = useRef<HTMLDivElement>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (window.google?.maps) {
      initializeMap();
      return;
    }
  }, []);

  // Google Map の初期化
  async function initializeMap() {
    if (!mapRef.current || !window.google) return;

    const { Map } = (await window.google.maps.importLibrary("maps")) as {
      Map: typeof google.maps.Map;
    };
    const { AdvancedMarkerElement } = (await window.google.maps.importLibrary(
      "marker"
    )) as {
      AdvancedMarkerElement: typeof google.maps.marker.AdvancedMarkerElement;
    };

    const map = new Map(mapRef.current!, {
      mapId: "map",
      center: { lat: 35.6895, lng: 139.6917 }, // 東京
      zoom: 10,
    });
    const marker = new AdvancedMarkerElement({
      title: "Tokyo",
      position: { lat: 35.6895, lng: 139.6917 },
      map,
    });
    const marker2 = new AdvancedMarkerElement({
      title: "Osaka",
      position: { lat: 34.6937, lng: 135.5023 },
      map,
    });
    console.log("Google Map initialized!", map);
    setIsLoaded(true);
  }

  return (
    <>
      <div style={{ width: "100%", height: "500px", position: "relative" }}>
        {!isLoaded && <Spinner />}
        <div ref={mapRef} style={{ width: "100%", height: "100%" }} />
      </div>
      <Script
        id="google-maps-script"
        src={`https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}`}
        strategy="beforeInteractive"
        onLoad={initializeMap} // ロード後に `handleScriptLoad` を実行
      />
    </>
  );
}
