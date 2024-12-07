from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from api.services import CertificateService
from api.interfaces.certificate import CertificateCreate, CertificateRead

certificate_router = APIRouter(prefix="/certificates")

@certificate_router.post("", status_code=status.HTTP_201_CREATED, response_model=CertificateRead)
async def create_certificate(
    info: CertificateCreate,
    service: CertificateService = Depends(CertificateService)
):
    """
    Create a certificate for a completed module.
    """
    return await service.create_certificate(info)

@certificate_router.get("/user/{user_id}")
async def get_user_certificates(
    user_id: UUID,
    service: CertificateService = Depends(CertificateService)
):
    """
    Retrieve all certificates for a specific user.
    """
    return await service.get_certificates_by_user(user_id)

@certificate_router.get("/{certificate_id}/download")
async def download_certificate(
    certificate_id: UUID,
    service: CertificateService = Depends(CertificateService)
):
    """
    Download a specific certificate PDF.
    """
    certificate = await service.get_certificate_by_id(certificate_id)
    
    if not certificate or not certificate.certificate_url:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    try:
        return FileResponse(
            certificate.certificate_url, 
            media_type='application/pdf', 
            filename=f'{certificate.module_name}_certificate.pdf'
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Certificate file not found")