# Luminus UE

Nuevo runtime 3D de **Luminus** sobre Unreal Engine.

Este repositorio reemplaza el experimento `Scanner`. El estado original del escáner se conserva en la rama `archive/scanner-original`.

## Objetivo inicial

Portar por comportamiento —no por traducción literal de JavaScript— las partes comprobadas de **Forest G 0.3.1**:

- escala y lectura del mundo;
- cámara de exploración;
- sprites 2D dentro de escenario 3D;
- texturas de terreno;
- agua, corriente y espuma costera;
- movimiento y colisión;
- vegetación/props a gran escala;
- streaming, LOD/HLOD e instancing.

## Regla de migración

Forest es la **referencia funcional y visual**. Unreal es la nueva implementación.

| Forest / Three.js | Luminus UE |
| --- | --- |
| JavaScript de runtime | C++ + Blueprint |
| THREE.Scene / Group | UWorld / AActor / USceneComponent |
| THREE.Mesh | UStaticMeshComponent / Landscape |
| InstancedMesh | UInstancedStaticMeshComponent / UHierarchicalInstancedStaticMeshComponent |
| sprites / sheets | Paper2D Sprite / Flipbook |
| materiales Three.js | Unreal Material / Material Instance |
| textura seamless + repeat | Texture2D + TextureCoordinate / material tiling |
| WaterBodySystem | Unreal Water + material propio de Luminus |
| espuma costera | material/mesh Niagara según cuerpo de agua |
| input teclado/touch | Enhanced Input |
| chunk streaming | World Partition |
| LOD propio | LOD + HLOD + World Partition |
| procedural de bioma | PCG + C++ |
| scripts de construcción | Python de Unreal Editor |

Python se usará para **automatizar el Editor e importar/generar assets**. No será lenguaje de gameplay.

## Estructura

```text
Luminus.uproject
Source/Luminus/                 runtime C++
Config/                         configuración
Content/Python/luminus/         automatización de Unreal Editor
Docs/Migration/                 contratos de migración Forest -> UE
```

## Primer milestone

**Forest G 0.3.1 parity slice**

1. Paper2D player visible en mundo 3D.
2. Cámara horizontal/orbit equivalente a Forest.
3. Un terreno de prueba con las texturas de Forest.
4. Río/lago/mar con el mismo lenguaje visual de agua y foam.
5. Un sector 128×128 con World Partition/instancing.
6. Métricas de FPS, draw calls y memoria antes de ampliar el mapa.

> La fuente exacta de Forest G 0.3.1 todavía debe fijarse por commit/archivo antes de copiar assets o reglas numéricas. No se usará una versión distinta por aproximación.
