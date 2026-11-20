import { useMemo } from "react";
import * as THREE from "three";
import type { SceneTimelineFrame } from "../types/forge";

export function Viewport3D({ frames }: { frames: SceneTimelineFrame[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const dronesRef = useRef<Array<{ g: THREE.Group; arrow: THREE.ArrowHelper }>>([]);
  const spheresRef = useRef<Array<{ m: THREE.Mesh; color: number }>>([]);

  useMemo(() => {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x09090b);
    const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 1000);
    camera.position.set(12, 9, -14);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    ref.current?.appendChild(renderer.domElement);
    // lights
    scene.add(new THREE.AmbientLight(0xffffff, 0.35));
    const sun = new THREE.DirectionalLight(0xffffff, 0.9);
    sun.position.set(0, 10, 5);
    scene.add(sun);

    let raf = 0;
    const loop = () => {
      raf = requestAnimationFrame(loop);
      renderer.render(scene, camera);
    };
    raf = requestAnimationFrame(loop);

    return () => {
      cancelAnimationFrame(raf);
      renderer.dispose();
      ref.current?.removeChild(renderer.domElement);
    };
  }, []);

  // render frames (simplified: last frame positions into drones + sphere states)
  const last = frames[frames.length - 1];
  return <div ref={ref} className="absolute inset-0" />;
}
