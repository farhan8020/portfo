from flask import Flask,render_template,request
from socket import gethostname
app = Flask(__name__)
import csv


# @app.route('/')   #a URL routing variable
# def my_home():  
#     return render_template('./index.html')

# # @app.route('/index.html')   
# # def home():  
# #     return render_template('./index.html')

# # @app.route('/project.html')   
# # def project():  
# #     return render_template('./project.html')

# # @app.route('/about.html')   
# # def about():  
# #     return render_template('./about.html')


@app.route('/')   
def my_home():  
    return render_template('./index.html')

@app.route('/<string:page_name>') #shotcut instead for many routes...apne aap click karne kar route honga page on website.
def about(page_name):  
    return render_template(page_name)

def write_to_file(data):                               #user ka data save karne ke liye database.txt file mein 
    with open('./database.txt', mode="a") as database: #append mode mei database.txt file open kiye
        fullname = data["fullname"]                    #niche ke route wala (data) hai yeh..jismei user ki info hai.
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n {fullname}, {email}, {subject}, {message}')  #yaha humne write kiye file ko.

def write_to_csv(data):                                
    with open('./database.csv', 'a', newline='') as database2:  #"/database.csv" file mei browser user ka data save honga isse
        fullname = data["fullname"]                    
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)    #syntax hai jaise ke waisa c/paste
        csv_writer.writerow([fullname,email,subject,message])       #function call karna honga niche          
        

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():                                 #yaha humne bataya ki agar hamara request POST hai..apna POST hi hai in"about.html'haina
    if request.method == 'POST':                   #user joh bhi enquiry ya data dalenga apne website par woh dict mei yaha display honga
        data = request.form.to_dict()              #humne user ke form ko data  ko assign kiye aur dictionary format mei print kiya 
        #print(data)
        #write_to_file(data)                        #call karna zaruri hai..tab hi database.txt file write hongi
        write_to_csv(data)
        return render_template('./thankyou.html')  #website kar output yeh aayanga aur yaha code mei apne ko user ka data print honga 
    else:                                          #backend terminal mein.
        return 'Something went wrong. Try again! '
    
if __name__ == "__main__":
   app.run(debug=True)

#if __name__ == '__main__':
    #if 'liveconsole' not in gethostname():
        #app.run()

#app.config['DEBUG'] = True

