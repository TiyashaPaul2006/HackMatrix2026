import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export const ThreatGlobeCanvas = () => {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let animId;
    const width = container.clientWidth || 600;
    const height = container.clientHeight || 550;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 0, 5.8);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 2. Base Earth Sphere (Dark cyber surface #0C1A2E)
    const globeRadius = 2.0;
    const sphereGeo = new THREE.SphereGeometry(globeRadius, 48, 48);
    const sphereMat = new THREE.MeshBasicMaterial({
      color: 0x0c1a2e,
      wireframe: false,
    });
    const globe = new THREE.Mesh(sphereGeo, sphereMat);
    scene.add(globe);

    // 3. Coordinate Wireframe Lattice (#1E3357)
    const wireGeo = new THREE.WireframeGeometry(new THREE.SphereGeometry(globeRadius * 1.002, 28, 28));
    const wireMat = new THREE.LineBasicMaterial({
      color: 0x1e3357,
      transparent: true,
      opacity: 0.45,
    });
    const wireframe = new THREE.LineSegments(wireGeo, wireMat);
    globe.add(wireframe);

    // 4. Custom Fresnel Atmosphere Shader (Lightweight 60+ FPS rim glow)
    const fresnelVertexShader = `
      varying vec3 vNormal;
      varying vec3 vPosition;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fresnelFragmentShader = `
      varying vec3 vNormal;
      varying vec3 vPosition;
      void main() {
        vec3 viewDir = normalize(-vPosition);
        float intensity = pow(1.0 - max(dot(vNormal, viewDir), 0.0), 3.0);
        gl_FragColor = vec4(0.0, 0.898, 1.0, 1.0) * intensity * 0.75;
      }
    `;

    const atmosphereGeo = new THREE.SphereGeometry(globeRadius * 1.15, 36, 36);
    const atmosphereMat = new THREE.ShaderMaterial({
      vertexShader: fresnelVertexShader,
      fragmentShader: fresnelFragmentShader,
      blending: THREE.AdditiveBlending,
      side: THREE.BackSide,
      transparent: true,
      depthWrite: false,
    });
    const atmosphere = new THREE.Mesh(atmosphereGeo, atmosphereMat);
    scene.add(atmosphere);

    // 5. Threat Nodes & Ingestion Trajectories
    // Generating simulated threat hotspots on coordinates (lat/lng to 3D)
    const latLngToVector3 = (lat, lng, radius) => {
      const phi = (90 - lat) * (Math.PI / 180);
      const theta = (lng + 180) * (Math.PI / 180);
      const x = -(radius * Math.sin(phi) * Math.cos(theta));
      const z = radius * Math.sin(phi) * Math.sin(theta);
      const y = radius * Math.cos(phi);
      return new THREE.Vector3(x, y, z);
    };

    const targetNodeCoords = [
      { lat: 37.77, lng: -122.41, type: 'legit' }, // SF
      { lat: 40.71, lng: -74.0, type: 'phish' },   // NYC
      { lat: 51.5, lng: -0.12, type: 'legit' },    // London
      { lat: 35.67, lng: 139.65, type: 'phish' },  // Tokyo
      { lat: 1.35, lng: 103.81, type: 'legit' },   // Singapore
      { lat: 28.61, lng: 77.20, type: 'phish' },   // Delhi
      { lat: -33.86, lng: 151.2, type: 'legit' },  // Sydney
      { lat: 55.75, lng: 37.61, type: 'phish' },   // Moscow
      { lat: -23.55, lng: -46.63, type: 'phish' }, // Sao Paulo
      { lat: 52.52, lng: 13.4, type: 'legit' },    // Berlin
    ];

    // Plot surface nodes
    const nodeGeometry = new THREE.SphereGeometry(0.035, 12, 12);
    targetNodeCoords.forEach((coord) => {
      const pos = latLngToVector3(coord.lat, coord.lng, globeRadius * 1.01);
      const color = coord.type === 'phish' ? 0xff3b3b : 0x00e5ff;
      const mat = new THREE.MeshBasicMaterial({ color });
      const mesh = new THREE.Mesh(nodeGeometry, mat);
      mesh.position.copy(pos);
      globe.add(mesh);
    });

    // Ingestion arcs using Quadratic Bezier Curves
    const arcsGroup = new THREE.Group();
    const packetParticles = [];

    for (let i = 0; i < targetNodeCoords.length - 1; i++) {
      const start = latLngToVector3(targetNodeCoords[i].lat, targetNodeCoords[i].lng, globeRadius);
      const nextIdx = (i + 3) % targetNodeCoords.length;
      const end = latLngToVector3(targetNodeCoords[nextIdx].lat, targetNodeCoords[nextIdx].lng, globeRadius);

      // Mid-point pushed outwards to form arched curve
      const mid = start.clone().add(end).multiplyScalar(0.5);
      const distance = start.distanceTo(end);
      mid.normalize().multiplyScalar(globeRadius + distance * 0.35);

      const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
      const points = curve.getPoints(36);
      const curveGeo = new THREE.BufferGeometry().setFromPoints(points);

      const isPhish = targetNodeCoords[i].type === 'phish';
      const curveColor = isPhish ? 0xff3b3b : 0x00e5ff;

      const curveMat = new THREE.LineBasicMaterial({
        color: curveColor,
        transparent: true,
        opacity: 0.35,
      });

      const line = new THREE.Line(curveGeo, curveMat);
      arcsGroup.add(line);

      // Add a flowing packet along the curve
      const packetMat = new THREE.MeshBasicMaterial({
        color: isPhish ? 0xff5e5e : 0x00ffff,
      });
      const packetMesh = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 8), packetMat);
      arcsGroup.add(packetMesh);

      packetParticles.push({
        curve,
        mesh: packetMesh,
        progress: Math.random(),
        speed: 0.005 + Math.random() * 0.007,
      });
    }

    globe.add(arcsGroup);

    // 6. Equatorial Threat Radar Sweep Ring
    const ringGeo = new THREE.RingGeometry(globeRadius * 1.05, globeRadius * 1.07, 64);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x00e5ff,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.4,
    });
    const radarRing = new THREE.Mesh(ringGeo, ringMat);
    radarRing.rotation.x = Math.PI / 2;
    globe.add(radarRing);

    // 7. Interactive Orbit & Mouse Controls
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    let targetRotation = { x: 0.25, y: -0.5 };
    let currentRotation = { x: 0.25, y: -0.5 };
    let mouseParallax = { x: 0, y: 0 };

    const onMouseDown = (e) => {
      isDragging = true;
      previousMousePosition = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e) => {
      // Camera parallax
      const rect = container.getBoundingClientRect();
      const xNorm = (e.clientX - rect.left) / rect.width - 0.5;
      const yNorm = (e.clientY - rect.top) / rect.height - 0.5;
      mouseParallax = { x: xNorm * 0.4, y: yNorm * 0.4 };

      if (!isDragging) return;
      const deltaX = e.clientX - previousMousePosition.x;
      const deltaY = e.clientY - previousMousePosition.y;

      targetRotation.y += deltaX * 0.005;
      targetRotation.x += deltaY * 0.005;

      // Clamp vertical rotation
      targetRotation.x = Math.max(-Math.PI * 0.4, Math.min(Math.PI * 0.4, targetRotation.x));

      previousMousePosition = { x: e.clientX, y: e.clientY };
    };

    const onMouseUp = () => { isDragging = false; };

    const domElement = renderer.domElement;
    domElement.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    // Touch support
    const onTouchStart = (e) => {
      if (e.touches.length === 1) {
        isDragging = true;
        previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      }
    };
    const onTouchMove = (e) => {
      if (isDragging && e.touches.length === 1) {
        const deltaX = e.touches[0].clientX - previousMousePosition.x;
        const deltaY = e.touches[0].clientY - previousMousePosition.y;
        targetRotation.y += deltaX * 0.006;
        targetRotation.x += deltaY * 0.006;
        previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      }
    };
    const onTouchEnd = () => { isDragging = false; };

    domElement.addEventListener('touchstart', onTouchStart, { passive: true });
    window.addEventListener('touchmove', onTouchMove, { passive: true });
    window.addEventListener('touchend', onTouchEnd);

    // Resize handling
    const onResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', onResize);

    // 8. Animation Render Loop (60+ FPS)
    const animate = () => {
      animId = requestAnimationFrame(animate);

      // Auto rotation when not dragging
      if (!isDragging) {
        targetRotation.y += 0.0018;
      }

      // Smooth lerp rotation
      currentRotation.x += (targetRotation.x - currentRotation.x) * 0.06;
      currentRotation.y += (targetRotation.y - currentRotation.y) * 0.06;

      globe.rotation.x = currentRotation.x;
      globe.rotation.y = currentRotation.y;

      // Parallax camera displacement
      camera.position.x += (mouseParallax.x - camera.position.x) * 0.05;
      camera.position.y += (-mouseParallax.y - camera.position.y) * 0.05;
      camera.lookAt(0, 0, 0);

      // Animate packet particles along arcs
      packetParticles.forEach((p) => {
        p.progress += p.speed;
        if (p.progress > 1.0) p.progress = 0.0;
        const point = p.curve.getPoint(p.progress);
        p.mesh.position.copy(point);
      });

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animId);
      domElement.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      domElement.removeEventListener('touchstart', onTouchStart);
      window.removeEventListener('touchmove', onTouchMove);
      window.removeEventListener('touchend', onTouchEnd);
      window.removeEventListener('resize', onResize);
      if (container.contains(domElement)) {
        container.removeChild(domElement);
      }
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className="w-full h-[450px] sm:h-[500px] lg:h-[580px] cursor-grab active:cursor-grabbing select-none relative"
    />
  );
};

export default ThreatGlobeCanvas;

