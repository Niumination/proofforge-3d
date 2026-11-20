import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { useForgeStore } from "../store/forgeStore";
import type { SceneTimelineFrame } from "../types/forge";

function clearGroup(group: THREE.Group) {
  while (group.children.length > 0) {
    const child = group.children[0];
    group.remove(child);
  }
}

export function Viewport3D({ frames }: { frames: SceneTimelineFrame[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const dynamicGroupRef = useRef<THREE.Group | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);

  const selectedScenario = useForgeStore((s) => s.selectedScenario);
  const activeTick = useForgeStore((s) => s.activeTick);
  const focusTrigger = useForgeStore((s) => s.focusTrigger);

  const safeTick = Math.min(activeTick, Math.max(frames.length - 1, 0));
  const activeFrame = frames[safeTick] ?? null;

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x09090b);
    scene.fog = new THREE.Fog(0x09090b, 40, 180);

    const camera = new THREE.PerspectiveCamera(
      52,
      Math.max(el.clientWidth, 1) / Math.max(el.clientHeight, 1),
      0.1,
      500
    );
    camera.position.set(10, 7, -12);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(el.clientWidth, el.clientHeight);
    el.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controlsRef.current = controls;

    scene.add(new THREE.GridHelper(160, 40, 0x27272a, 0x18181b));
    scene.add(new THREE.AmbientLight(0xffffff, 0.55));
    const dir = new THREE.DirectionalLight(0xffffff, 1.0);
    dir.position.set(8, 16, 10);
    scene.add(dir);

    const dynamicGroup = new THREE.Group();
    scene.add(dynamicGroup);
    dynamicGroupRef.current = dynamicGroup;

    const resizeObserver = new ResizeObserver(() => {
      if (!el) return;
      const w = Math.max(el.clientWidth, 1);
      const h = Math.max(el.clientHeight, 1);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    });
    resizeObserver.observe(el);

    let raf = 0;
    const animate = () => {
      raf = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    raf = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(raf);
      resizeObserver.disconnect();
      controls.dispose();
      renderer.dispose();
      if (renderer.domElement.parentNode === el) {
        el.removeChild(renderer.domElement);
      }
    };
  }, []);

  // Re-frame camera when scenario changes or focus violation is triggered
  useEffect(() => {
    const cam = cameraRef.current;
    const ctrl = controlsRef.current;
    if (!cam || !ctrl) return;
    if (selectedScenario === "drone_swarm") {
      const zFocus = activeFrame?.entities[0]?.position[2] ?? 0;
      cam.position.set(6.5, 4.5, zFocus - 7.5);
      ctrl.target.set(0.2, 0.8, zFocus);
    } else if (selectedScenario === "robot_arm") {
      cam.position.set(0.5, 0.7, 1.6);
      ctrl.target.set(0.3, 0.35, 0);
    } else {
      cam.position.set(5.5, 4.8, 6.2);
      ctrl.target.set(1.5, 1.2, 1.0);
    }
    ctrl.update();
  }, [selectedScenario, focusTrigger]);

  // Render active frame entities + constraints_overlay
  useEffect(() => {
    const group = dynamicGroupRef.current;
    if (!group) return;
    clearGroup(group);

    if (!activeFrame) return;

    if (selectedScenario === "drone_swarm") {
      // Draw path guidelines for drone trajectories
      if (frames.length > 1) {
        [0, 1].forEach((idx) => {
          const pts = frames
            .map((f) => f.entities[idx]?.position)
            .filter(Boolean)
            .map((p) => new THREE.Vector3(p[0], 0.06, p[2]));
          if (pts.length > 1) {
            const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
            const lineMat = new THREE.LineBasicMaterial({
              color: idx === 0 ? 0x22d3ee : 0xf59e0b,
              transparent: true,
              opacity: 0.35,
            });
            group.add(new THREE.Line(lineGeo, lineMat));
          }
        });
      }

      activeFrame.entities.forEach((ent, i) => {
        const col = i === 0 ? 0x22d3ee : 0xf59e0b;
        const drone = new THREE.Group();
        const body = new THREE.Mesh(
          new THREE.BoxGeometry(0.55, 0.16, 0.55),
          new THREE.MeshStandardMaterial({ color: col, emissive: col, emissiveIntensity: 0.35 })
        );
        drone.add(body);
        [
          [-0.3, -0.3],
          [0.3, -0.3],
          [-0.3, 0.3],
          [0.3, 0.3],
        ].forEach(([dx, dz]) => {
          const rotor = new THREE.Mesh(
            new THREE.CylinderGeometry(0.16, 0.16, 0.02, 14),
            new THREE.MeshStandardMaterial({ color: 0xe4e4e7, transparent: true, opacity: 0.7 })
          );
          rotor.position.set(dx, 0.1, dz);
          drone.add(rotor);
        });
        drone.position.set(ent.position[0], ent.position[1], ent.position[2]);
        group.add(drone);
      });
    } else if (selectedScenario === "robot_arm") {
      // Table danger plane y = 0.15m
      const table = new THREE.Mesh(
        new THREE.BoxGeometry(2.0, 0.02, 1.2),
        new THREE.MeshStandardMaterial({ color: 0xef4444, transparent: true, opacity: 0.18 })
      );
      table.position.set(0.3, 0.14, 0);
      group.add(table);

      const pts = activeFrame.entities.map((e) => new THREE.Vector3(...e.position));
      if (activeFrame.entities[2]?.meta?.prev) {
        const p2 = activeFrame.entities[2].meta.prev as number[];
        pts.splice(2, 0, new THREE.Vector3(p2[0], p2[1], p2[2]));
      }
      if (pts.length >= 2) {
        const linkGeo = new THREE.BufferGeometry().setFromPoints(pts);
        const linkMat = new THREE.LineBasicMaterial({ color: 0x22d3ee });
        group.add(new THREE.Line(linkGeo, linkMat));
      }
      activeFrame.entities.forEach((ent) => {
        const isBreach = ent.status === "TORQUE_BREACH";
        const mesh = new THREE.Mesh(
          new THREE.SphereGeometry(ent.kind === "arm_effector" ? 0.045 : 0.055, 16, 16),
          new THREE.MeshStandardMaterial({
            color: isBreach ? 0xef4444 : 0x22d3ee,
            emissive: isBreach ? 0xef4444 : 0x0891b2,
            emissiveIntensity: 0.45,
          })
        );
        mesh.position.set(ent.position[0], ent.position[1], ent.position[2]);
        group.add(mesh);
      });
    } else {
      // 4x4x4 grid wireframe markers
      for (let x = 0; x < 4; x++) {
        for (let y = 0; y < 4; y++) {
          for (let z = 0; z < 4; z++) {
            const cell = new THREE.Mesh(
              new THREE.BoxGeometry(0.82, 0.82, 0.82),
              new THREE.MeshBasicMaterial({
                color: 0x27272a,
                wireframe: true,
                transparent: true,
                opacity: 0.25,
              })
            );
            cell.position.set(x, y, z);
            group.add(cell);
          }
        }
      }
      const colors = [0x22d3ee, 0xf59e0b, 0xa855f7, 0x3b82f6];
      activeFrame.entities.forEach((ent, i) => {
        const deadlocked = ent.status === "DEADLOCK";
        const cube = new THREE.Mesh(
          new THREE.BoxGeometry(0.6, 0.6, 0.6),
          new THREE.MeshStandardMaterial({
            color: deadlocked ? 0xef4444 : colors[i % colors.length],
            emissive: deadlocked ? 0xef4444 : colors[i % colors.length],
            emissiveIntensity: deadlocked ? 0.6 : 0.25,
          })
        );
        cube.position.set(ent.position[0], ent.position[1], ent.position[2]);
        group.add(cube);
      });
    }

    // Safety spheres / constraint overlays
    activeFrame.constraints_overlay.forEach((ov) => {
      const sphere = new THREE.Mesh(
        new THREE.SphereGeometry(ov.radius, 20, 14),
        new THREE.MeshBasicMaterial({
          color: ov.breached ? 0xef4444 : 0x22c55e,
          wireframe: true,
          transparent: true,
          opacity: ov.breached ? 0.65 : 0.28,
        })
      );
      sphere.position.set(ov.center[0], ov.center[1], ov.center[2]);
      group.add(sphere);
    });
  }, [activeFrame, frames, selectedScenario]);

  const isViolated = activeFrame?.is_violation ?? false;

  return (
    <div className="relative w-full h-full">
      <div ref={containerRef} className="absolute inset-0" />
      {isViolated && (
        <>
          <div
            className="fixed inset-0 pointer-events-none z-20 pf-flash"
            style={{ boxShadow: "inset 0 0 140px 35px rgba(239,68,68,0.45)" }}
          />
          <div className="absolute top-3 left-1/2 -translate-x-1/2 z-30 px-4 py-2 rounded-lg bg-red-600/90 text-white text-xs font-extrabold shadow-xl">
            ⚠ SAT_VIOLATION · Frame #{activeFrame?.tick} (t = {activeFrame?.time_sec}s)
          </div>
        </>
      )}
      {!activeFrame && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="rounded-xl border border-zinc-800 bg-zinc-950/80 px-5 py-3 text-xs text-zinc-400">
            Click <strong className="text-cyan-400">Run ProofForge Pipeline</strong> to execute Z3 and render 3D trace.
          </div>
        </div>
      )}
    </div>
  );
}
