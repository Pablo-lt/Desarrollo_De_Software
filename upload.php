<?php
// Directorio donde se guardarán los archivos multimedia
$targetDir = "uploads/";

if (!empty($_FILES['file'])) {
    $fileName = basename($_FILES['file']['name']);
    $targetPath = $targetDir . $fileName;
    $fileType = pathinfo($targetPath, PATHINFO_EXTENSION);

    // Mover el archivo al directorio de destino
    if (move_uploaded_file($_FILES['file']['tmp_name'], $targetPath)) {
        // Determinar el tipo de archivo y retornar el contenido categorizado
        $fileType = strtolower($fileType);
        switch ($fileType) {
            case 'jpg':
            case 'jpeg':
            case 'png':
                echo '<img src="' . $targetPath . '" alt="Imagen">';
                break;
            case 'mp4':
            case 'webm':
            case 'ogg':
                echo '<video controls><source src="' . $targetPath . '" type="video/' . $fileType . '"></video>';
                break;
            case 'mp3':
            case 'wav':
                echo '<audio controls><source src="' . $targetPath . '" type="audio/' . $fileType . '"></audio>';
                break;
            default:
                echo 'Archivo no soportado';
                break;
        }
    } else {
        echo 'Error al subir el archivo';
    }
}
?>
