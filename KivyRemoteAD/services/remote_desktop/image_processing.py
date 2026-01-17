import cv2
import numpy as np
from PIL import Image
import io

class ImageProcessing:
    def __init__(self, quality=80, compression='jpeg'):
        self.quality = quality
        self.compression = compression.lower()
        
    def compress_image(self, img):
        """压缩图像
        
        Args:
            img: numpy数组，RGB格式
            
        Returns:
            压缩后的图像数据（bytes）
        """
        if img is None:
            return None
            
        try:
            if self.compression == 'jpeg':
                # 使用OpenCV压缩为JPEG
                result, encimg = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_RGB2BGR), 
                                           [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])
                if result:
                    return encimg.tobytes()
            elif self.compression == 'png':
                # 使用OpenCV压缩为PNG
                result, encimg = cv2.imencode('.png', cv2.cvtColor(img, cv2.COLOR_RGB2BGR),
                                           [int(cv2.IMWRITE_PNG_COMPRESSION), 3])
                if result:
                    return encimg.tobytes()
            elif self.compression == 'webp':
                # 使用PIL压缩为WebP
                pil_img = Image.fromarray(img)
                buffer = io.BytesIO()
                pil_img.save(buffer, format='WebP', quality=self.quality)
                return buffer.getvalue()
            
            # 默认使用JPEG
            result, encimg = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_RGB2BGR),
                                       [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])
            if result:
                return encimg.tobytes()
            
            return None
        except Exception as e:
            print(f"Image compression error: {e}")
            return None
            
    def decompress_image(self, img_data):
        """解压缩图像
        
        Args:
            img_data: 压缩后的图像数据（bytes）
            
        Returns:
            numpy数组，RGB格式
        """
        if not img_data:
            return None
            
        try:
            # 使用OpenCV解码图像
            img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
            if img is not None:
                # 转换为RGB格式
                return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # 尝试使用PIL解码
            pil_img = Image.open(io.BytesIO(img_data))
            return np.array(pil_img)
        except Exception as e:
            print(f"Image decompression error: {e}")
            return None
            
    def resize_image(self, img, width=None, height=None, keep_ratio=True):
        """调整图像大小
        
        Args:
            img: numpy数组，RGB格式
            width: 目标宽度
            height: 目标高度
            keep_ratio: 是否保持宽高比
            
        Returns:
            调整大小后的图像
        """
        if img is None:
            return None
            
        try:
            h, w = img.shape[:2]
            
            if not width and not height:
                return img
            
            if keep_ratio:
                if width and not height:
                    # 按宽度缩放
                    ratio = width / w
                    new_w = width
                    new_h = int(h * ratio)
                elif height and not width:
                    # 按高度缩放
                    ratio = height / h
                    new_h = height
                    new_w = int(w * ratio)
                else:
                    # 按较小的比例缩放
                    ratio = min(width / w, height / h)
                    new_w = int(w * ratio)
                    new_h = int(h * ratio)
            else:
                # 不保持宽高比
                new_w = width if width else w
                new_h = height if height else h
            
            # 使用OpenCV调整大小
            resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            return resized_img
        except Exception as e:
            print(f"Image resize error: {e}")
            return None
            
    def convert_to_grayscale(self, img):
        """转换为灰度图像
        
        Args:
            img: numpy数组，RGB格式
            
        Returns:
            灰度图像
        """
        if img is None:
            return None
            
        try:
            return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        except Exception as e:
            print(f"Grayscale conversion error: {e}")
            return None
            
    def get_image_info(self, img_data):
        """获取图像信息
        
        Args:
            img_data: 压缩后的图像数据（bytes）
            
        Returns:
            图像信息字典，包含宽度、高度、通道数等
        """
        try:
            img = self.decompress_image(img_data)
            if img is not None:
                h, w = img.shape[:2]
                channels = img.shape[2] if len(img.shape) > 2 else 1
                return {
                    'width': w,
                    'height': h,
                    'channels': channels,
                    'size': len(img_data),
                    'format': self.compression
                }
            return None
        except Exception as e:
            print(f"Get image info error: {e}")
            return None
            
    def set_quality(self, quality):
        """设置压缩质量
        
        Args:
            quality: 压缩质量，0-100
        """
        self.quality = max(0, min(100, quality))
        
    def set_compression(self, compression):
        """设置压缩格式
        
        Args:
            compression: 压缩格式，'jpeg'、'png'或'webp'
        """
        self.compression = compression.lower()

if __name__ == "__main__":
    # 测试图像处理功能
    from screen_capture import ScreenCapture
    
    sc = ScreenCapture()
    img = sc.capture()
    
    if img is not None:
        ip = ImageProcessing(quality=80, compression='jpeg')
        
        # 压缩图像
        compressed = ip.compress_image(img)
        print(f"Original size: {img.nbytes} bytes")
        print(f"Compressed size: {len(compressed)} bytes")
        print(f"Compression ratio: {len(compressed)/img.nbytes:.2f}")
        
        # 解压缩图像
        decompressed = ip.decompress_image(compressed)
        print(f"Decompressed shape: {decompressed.shape}")
        
        # 调整大小
        resized = ip.resize_image(img, width=640)
        print(f"Resized shape: {resized.shape}")
        
        # 获取图像信息
        info = ip.get_image_info(compressed)
        print(f"Image info: {info}")
