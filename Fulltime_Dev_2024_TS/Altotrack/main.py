import threading
from services.fulltrack_service import main
from services.Altotrack_service import Altotrack_service

if __name__ == "__main__":

    fulltrack_thread = threading.Thread(target=main)
    fulltrack_thread.start()
    
    Altotrack_service()

    fulltrack_thread.join()
