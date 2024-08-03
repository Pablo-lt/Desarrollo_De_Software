from app.models import User, UserData

class Utils(): 
      
    def __init__(self):

        self.USERNAME_PRUEBA = 'pabloprats'
        self.EMAIL_PRUEBA = 'test@test.com'
        self.PASSWORD_PRUEBA = '123456'
        self.FIRSTNAME_PRUEBA = 'Pablo'
        self.LASTNAME_PRUEBA = 'Prats'
        self.PHONE_PRUEBA = '54260123456789'
        self.DESCRIPTION = 'DKJSNFJNSKJFNSKJDNFJNJDS'


    def create_test_user(self):
        data = UserData()
        data.firstname = self.FIRSTNAME_PRUEBA
        data.lastname = self.LASTNAME_PRUEBA
        data.phone = self.PHONE_PRUEBA
        data.description = self.DESCRIPTION 

        user = User()
        user.data = data
        user.username = self.USERNAME_PRUEBA
        user.email = self.EMAIL_PRUEBA
        user.password = self.PASSWORD_PRUEBA
        
        return user
    
#Se crea una instancia de Utils para uso global

utils= Utils()