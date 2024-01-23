from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from fastapi import HTTPException

class TwilioService:
    def __init__(self, account_sid, auth_token, service_sid):
        self.client = Client(account_sid, auth_token)
        self.service_sid = service_sid

    def send_otp(self, to_number: str):
        try:
            verification = self.client.verify.services(self.service_sid).verifications.create(
                to="+91" + to_number,
                channel='sms'  # You can also use 'call' or 'email' here
            )
            return verification.sid
        except TwilioRestException as e:
            raise HTTPException(status_code=500, detail=f"Error sending OTP: {str(e)}") from e
        
    def verify_otp(self, to_number, otp):
        try:
            verification_check = self.client.verify.services(self.service_sid).verification_checks.create(
                to="+91" + to_number,
                code=otp
            )
            return verification_check.status
        except TwilioRestException as e:
            raise HTTPException(status_code=500, detail=f"Error verifying OTP: {str(e)}") from e
