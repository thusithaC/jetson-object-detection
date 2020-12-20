from jetcam.csi_camera import CSICamera
import logging

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def get_camera(width=224, height=224, capture_device=0, capture_fps=24):
    camera = CSICamera(width=width, height=height, capture_device=capture_device, capture_fps=capture_fps)
    return camera

def close_camera(camera):
    if camera:
        camera.running = False
        camera.cap.release()
    return


def display_camera_widget(camera, stream=False):
    """For jupyter debugging"""
    import ipywidgets
    from IPython.display import display
    from jetcam.utils import bgr8_to_jpeg
    image_widget = ipywidgets.Image(format='jpeg')
    display(image_widget) 
    if stream:
        def update_image(change):
            image = change['new']
            image_widget.value = bgr8_to_jpeg(image)
               
        camera.running = True
        camera.observe(update_image, names='value')
        return update_image
    else:
        image = camera.read()
        logger.info(f"Obtained image {image.shape}")
        image_widget.value = bgr8_to_jpeg(image)
        return
    

def close_camera_widget(camera, handle):
    camera.unobserve(handle, names='value')

