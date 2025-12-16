/**
 * Minecraft Schematic Builder - Optimized 3D Viewer
 * Features: Instanced rendering, smooth controls, view presets
 */

// Three.js scene components
let scene, camera, renderer, controls;
let instancedMesh, edgesMesh;
let gridHelper;
let currentSchematic = null;

// API base URL
const API_BASE = 'http://localhost:5000/api';

// Performance settings
const USE_INSTANCED_RENDERING = true;
const MAX_INSTANCES = 100000;

// Initialize the 3D viewer with optimizations
function init3DViewer() {
    const container = document.getElementById('viewer3d');

    // Create scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB); // Sky blue

    // Create camera
    const aspect = container.clientWidth / container.clientHeight;
    camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 2000);
    camera.position.set(20, 20, 20);
    camera.lookAt(0, 0, 0);

    // Create renderer with optimizations
    renderer = new THREE.WebGLRenderer({
        antialias: true,
        powerPreference: "high-performance"
    });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Limit pixel ratio for performance
    renderer.shadowMap.enabled = false; // Disable shadows for better performance
    container.appendChild(renderer.domElement);

    // Add orbit controls with improved settings
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08; // Smoother damping
    controls.rotateSpeed = 0.8;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;
    controls.minDistance = 5;
    controls.maxDistance = 500;
    controls.enablePan = true;
    controls.mouseButtons = {
        LEFT: THREE.MOUSE.ROTATE,
        MIDDLE: THREE.MOUSE.DOLLY,
        RIGHT: THREE.MOUSE.PAN
    };

    // Add enhanced lighting for better color visibility
    // Ambient light provides base illumination
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    // Hemisphere light for natural sky/ground lighting
    const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.4);
    scene.add(hemisphereLight);

    // Main directional light from top-right
    const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.6);
    directionalLight1.position.set(10, 20, 10);
    scene.add(directionalLight1);

    // Secondary directional light from opposite side for fill
    const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.3);
    directionalLight2.position.set(-10, 10, -10);
    scene.add(directionalLight2);

    // Add grid helper
    gridHelper = new THREE.GridHelper(100, 100, 0x888888, 0xcccccc);
    scene.add(gridHelper);

    // Handle window resize
    window.addEventListener('resize', onWindowResize);

    // Add keyboard shortcuts for view presets
    window.addEventListener('keydown', handleKeyPress);

    // Start animation loop
    animate();
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

function onWindowResize() {
    const container = document.getElementById('viewer3d');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

// Handle keyboard shortcuts
function handleKeyPress(e) {
    if (!currentSchematic) return;

    const { width, height, length } = currentSchematic;
    const centerX = width / 2;
    const centerY = height / 2;
    const centerZ = length / 2;
    const maxDim = Math.max(width, height, length);
    const distance = maxDim * 2;

    switch (e.key) {
        case '1': // Top view
            camera.position.set(centerX, centerY + distance, centerZ);
            controls.target.set(centerX, centerY, centerZ);
            break;
        case '2': // Front view
            camera.position.set(centerX, centerY, centerZ + distance);
            controls.target.set(centerX, centerY, centerZ);
            break;
        case '3': // Side view
            camera.position.set(centerX + distance, centerY, centerZ);
            controls.target.set(centerX, centerY, centerZ);
            break;
        case '4': // Isometric view
            camera.position.set(centerX + distance, centerY + distance, centerZ + distance);
            controls.target.set(centerX, centerY, centerZ);
            break;
    }
}

// Clear all blocks from the scene
function clearScene() {
    // Remove instanced meshes
    if (window.instancedMeshes) {
        window.instancedMeshes.forEach(mesh => {
            scene.remove(mesh);
            mesh.geometry.dispose();
            mesh.material.dispose();
        });
    }
    window.instancedMeshes = [];

    // Remove edges meshes
    if (window.edgesMeshes) {
        window.edgesMeshes.forEach(mesh => {
            scene.remove(mesh);
            mesh.geometry.dispose();
            mesh.material.dispose();
        });
    }
    window.edgesMeshes = [];

    // Legacy cleanup (just in case)
    if (typeof instancedMesh !== 'undefined' && instancedMesh) {
        scene.remove(instancedMesh);
        if (instancedMesh.geometry) instancedMesh.geometry.dispose();
        if (instancedMesh.material) instancedMesh.material.dispose();
        instancedMesh = null;
    }
    if (typeof edgesMesh !== 'undefined' && edgesMesh) {
        scene.remove(edgesMesh);
        if (edgesMesh.geometry) edgesMesh.geometry.dispose();
        if (edgesMesh.material) edgesMesh.material.dispose();
        edgesMesh = null;
    }

    currentSchematic = null;
    updateSchematicInfo(null);
}

// Optimized rendering using instanced meshes
function renderSchematic(schematicData) {
    clearScene();

    if (!schematicData || !schematicData.blocks || schematicData.blocks.length === 0) {
        return;
    }

    currentSchematic = schematicData;
    const { width, height, length, blocks } = schematicData;

    // Split blocks into chunks to handle very large schematics
    const CHUNK_SIZE = 100000;

    for (let i = 0; i < blocks.length; i += CHUNK_SIZE) {
        const chunk = blocks.slice(i, i + CHUNK_SIZE);
        renderChunk(chunk);
    }

    // Center camera on schematic
    const centerX = width / 2;
    const centerY = height / 2;
    const centerZ = length / 2;

    controls.target.set(centerX, centerY, centerZ);

    // Position camera to see entire schematic
    const maxDim = Math.max(width, height, length);
    const distance = maxDim * 2;
    camera.position.set(
        centerX + distance,
        centerY + distance,
        centerZ + distance
    );

    // Update grid position and size
    const gridSize = Math.max(100, maxDim * 2);
    scene.remove(gridHelper);
    gridHelper = new THREE.GridHelper(gridSize, Math.min(100, gridSize), 0x888888, 0xcccccc);
    gridHelper.position.set(centerX, 0, centerZ);
    scene.add(gridHelper);

    updateSchematicInfo(schematicData);
}

// Render a chunk of blocks using instancing
function renderChunk(blocks) {
    const geometry = new THREE.BoxGeometry(1, 1, 1);

    // Use MeshPhongMaterial for better lighting and color support with instances
    // Note: Do NOT use vertexColors here - instanceColor is handled separately
    const material = new THREE.MeshPhongMaterial({
        color: 0xffffff,  // Base color will be multiplied by instance color
        flatShading: true
    });

    // Create instanced mesh
    const mesh = new THREE.InstancedMesh(geometry, material, blocks.length);
    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);

    const matrix = new THREE.Matrix4();
    const color = new THREE.Color();

    // Set positions and colors for each block
    blocks.forEach((block, i) => {
        const { x, y, z, color: blockColor } = block;

        // Set position
        matrix.setPosition(x, y, z);
        mesh.setMatrixAt(i, matrix);

        // Set color - setColorAt will create instanceColor if needed
        if (blockColor && Array.isArray(blockColor)) {
            color.setRGB(blockColor[0] / 255, blockColor[1] / 255, blockColor[2] / 255);
        } else {
            // Default gray color if no color provided
            color.setRGB(0.5, 0.5, 0.5);
        }
        mesh.setColorAt(i, color);
    });

    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) {
        mesh.instanceColor.needsUpdate = true;
    }

    scene.add(mesh);

    // Store in global array (needs to be initialized in clearScene)
    if (!window.instancedMeshes) window.instancedMeshes = [];
    window.instancedMeshes.push(mesh);

    // Add edges for better block definition and visibility
    // Only add edges if the chunk is small enough to avoid performance issues
    if (blocks.length < 20000) {
        const edgesGeometry = new THREE.EdgesGeometry(geometry);
        const edgesMaterial = new THREE.LineBasicMaterial({
            color: 0x000000,
            opacity: 0.15,
            transparent: true,
            linewidth: 1
        });

        const edgesMesh = new THREE.InstancedMesh(
            edgesGeometry,
            edgesMaterial,
            blocks.length
        );

        blocks.forEach((block, i) => {
            const { x, y, z } = block;
            matrix.setPosition(x, y, z);
            edgesMesh.setMatrixAt(i, matrix);
        });

        edgesMesh.instanceMatrix.needsUpdate = true;
        scene.add(edgesMesh);

        if (!window.edgesMeshes) window.edgesMeshes = [];
        window.edgesMeshes.push(edgesMesh);
    }
}

// Update schematic info display
function updateSchematicInfo(schematicData) {
    if (schematicData) {
        document.getElementById('dimensions').textContent =
            `${schematicData.width} × ${schematicData.height} × ${schematicData.length}`;
        document.getElementById('blockCount').textContent = schematicData.block_count;
    } else {
        document.getElementById('dimensions').textContent = '-';
        document.getElementById('blockCount').textContent = '0';
    }
}

// Show status message
function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('statusMessage');
    statusEl.textContent = message;
    statusEl.className = `status-message ${type}`;

    // Auto-hide after 5 seconds
    setTimeout(() => {
        statusEl.textContent = '';
        statusEl.className = 'status-message';
    }, 5000);
}

// Execute code
async function executeCode() {
    const code = document.getElementById('codeEditor').value;

    if (!code.trim()) {
        showStatus('Please enter some code first', 'error');
        return;
    }

    showStatus('Executing code...', 'info');

    try {
        const response = await fetch(`${API_BASE}/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code })
        });

        const data = await response.json();

        if (data.success) {
            renderSchematic(data.schematic);
            showStatus(data.message, 'success');
        } else {
            showStatus('Execution failed. See details below.', 'error');
            showErrorModal(data.error, data.traceback);
            console.error('Execution error:', data.traceback);
        }
    } catch (error) {
        showStatus(`Network error: ${error.message}`, 'error');
        console.error('Network error:', error);
    }
}

// Export schematic
async function exportSchematic() {
    console.log('Export button clicked');
    console.log('Current schematic:', currentSchematic);

    // Check if a schematic has been created
    if (!currentSchematic) {
        console.log('No schematic found');
        showStatus('Please run your code first to create a schematic before exporting!', 'error');
        return;
    }

    console.log('Showing filename modal...');

    // Show custom filename modal instead of prompt()
    const filenameModal = document.getElementById('filenameModal');
    const filenameInput = document.getElementById('filenameInput');
    filenameInput.value = 'my_structure';
    filenameModal.style.display = 'flex';

    // Focus the input and select all text
    setTimeout(() => {
        filenameInput.focus();
        filenameInput.select();
    }, 100);
}


// Perform the actual export with the given filename
async function performExport(filename) {
    console.log('[EXPORT] Performing export with filename:', filename);

    if (!filename || !filename.trim()) {
        console.log('[EXPORT] Empty filename provided');
        showStatus('Please enter a valid filename', 'error');
        return;
    }

    showStatus('Exporting schematic...', 'info');
    console.log('[EXPORT] Sending request to server...');

    try {
        const response = await fetch(`${API_BASE}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ filename: filename.trim() })
        });

        console.log('[EXPORT] Response status:', response.status, response.statusText);
        console.log('[EXPORT] Response content-type:', response.headers.get('content-type'));

        if (response.ok) {
            // Check if the response is actually a file or an error JSON
            const contentType = response.headers.get('content-type');

            if (contentType && contentType.includes('application/json')) {
                // Server returned JSON (likely an error)
                const data = await response.json();
                console.error('[EXPORT] Server returned JSON instead of file:', data);
                showStatus(`Export error: ${data.error || 'Unknown error'}`, 'error');
                return;
            }

            console.log('[EXPORT] Creating blob...');
            const responseBlob = await response.blob();
            console.log('[EXPORT] Response blob size:', responseBlob.size, 'bytes');

            // Create a new blob with explicit type to ensure proper handling
            const blob = new Blob([responseBlob], { type: 'application/octet-stream' });
            console.log('[EXPORT] Blob created, size:', blob.size, 'bytes');

            const downloadFilename = filename.endsWith('.schem') ? filename : `${filename}.schem`;
            console.log('[EXPORT] Download filename:', downloadFilename);

            // Create download link with proper attributes
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = downloadFilename;
            a.setAttribute('download', downloadFilename); // Ensure attribute is set

            document.body.appendChild(a);
            console.log('[EXPORT] Triggering download...');
            a.click();

            // Cleanup after a short delay to ensure download starts
            setTimeout(() => {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                console.log('[EXPORT] Cleanup complete');
            }, 100);

            showStatus('Schematic exported successfully! File saved to your Downloads folder.', 'success');
        } else {
            const data = await response.json();
            console.error('[EXPORT] Server error:', data);
            showStatus(`Export error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('[EXPORT] Exception:', error);
        showStatus(`Network error: ${error.message}`, 'error');
    }
}

// Show error modal with details
function showErrorModal(error, traceback) {
    const errorText = document.getElementById('errorText');
    errorText.textContent = `Error: ${error}\n\nTraceback:\n${traceback}`;
    document.getElementById('errorModal').style.display = 'flex';
}

// Load examples
async function loadExamples() {
    try {
        const response = await fetch(`${API_BASE}/examples`);
        const data = await response.json();

        const examplesList = document.getElementById('examplesList');
        examplesList.innerHTML = '';

        data.examples.forEach(example => {
            const exampleDiv = document.createElement('div');
            exampleDiv.className = 'example-item';
            exampleDiv.innerHTML = `
                <h3>${example.name}</h3>
                <p>${example.description}</p>
                <button class="btn btn-primary" onclick="loadExampleCode(${JSON.stringify(example.code).replace(/"/g, '&quot;')})">
                    Load This Example
                </button>
            `;
            examplesList.appendChild(exampleDiv);
        });

        document.getElementById('examplesModal').style.display = 'flex';
    } catch (error) {
        showStatus(`Failed to load examples: ${error.message}`, 'error');
    }
}

function loadExampleCode(code) {
    document.getElementById('codeEditor').value = code;
    document.getElementById('examplesModal').style.display = 'none';
    showStatus('Example loaded! Click Run to preview.', 'success');
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    init3DViewer();

    document.getElementById('runCode').addEventListener('click', executeCode);

    // Use capture phase and stop propagation to prevent extension interference
    const exportBtn = document.getElementById('exportSchem');
    exportBtn.addEventListener('click', function (e) {
        e.stopImmediatePropagation(); // Stop extension handlers
        e.preventDefault();
        console.log('Export button clicked - calling exportSchematic()');
        exportSchematic();
    }, true); // Use capture phase

    document.getElementById('clearView').addEventListener('click', clearScene);
    document.getElementById('loadExample').addEventListener('click', loadExamples);
    document.getElementById('closeModal').addEventListener('click', () => {
        document.getElementById('examplesModal').style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        const examplesModal = document.getElementById('examplesModal');
        const errorModal = document.getElementById('errorModal');
        if (e.target === examplesModal) {
            examplesModal.style.display = 'none';
        }
        if (e.target === errorModal) {
            errorModal.style.display = 'none';
        }
    });

    // Error modal controls
    document.getElementById('closeErrorModal').addEventListener('click', () => {
        document.getElementById('errorModal').style.display = 'none';
    });

    document.getElementById('copyErrorBtn').addEventListener('click', () => {
        const errorText = document.getElementById('errorText').innerText;
        navigator.clipboard.writeText(errorText).then(() => {
            const btn = document.getElementById('copyErrorBtn');
            const originalText = btn.textContent;
            btn.textContent = '✅ Copied to Clipboard!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        }).catch(err => {
            showStatus('Failed to copy error', 'error');
            console.error('Copy failed:', err);
        });
    });

    // Keyboard shortcuts
    document.getElementById('codeEditor').addEventListener('keydown', (e) => {
        // Ctrl+Enter to run
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            executeCode();
        }

        // Tab support in textarea
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = e.target.selectionStart;
            const end = e.target.selectionEnd;
            e.target.value = e.target.value.substring(0, start) + '    ' + e.target.value.substring(end);
            e.target.selectionStart = e.target.selectionEnd = start + 4;
        }
    });

    // Filename modal controls
    document.getElementById('confirmExport').addEventListener('click', () => {
        const filename = document.getElementById('filenameInput').value;
        document.getElementById('filenameModal').style.display = 'none';
        performExport(filename);
    });

    document.getElementById('cancelExport').addEventListener('click', () => {
        document.getElementById('filenameModal').style.display = 'none';
        showStatus('Export cancelled', 'info');
    });

    document.getElementById('closeFilenameModal').addEventListener('click', () => {
        document.getElementById('filenameModal').style.display = 'none';
        showStatus('Export cancelled', 'info');
    });

    // Allow Enter key to confirm export
    document.getElementById('filenameInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const filename = document.getElementById('filenameInput').value;
            document.getElementById('filenameModal').style.display = 'none';
            performExport(filename);
        } else if (e.key === 'Escape') {
            document.getElementById('filenameModal').style.display = 'none';
            showStatus('Export cancelled', 'info');
        }
    });

    // Show controls hint
    showStatus('Controls: Left-click to rotate, Right-click to pan, Scroll to zoom. Keys 1-4 for view presets.', 'info');
});
