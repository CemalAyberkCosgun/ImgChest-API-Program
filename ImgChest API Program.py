# Imports
import io
import json
import requests
import os

#Function definitions:
def askAgain():
    wow = input("Is there anything else you'd like that to do? [y/n] ")
    match wow.lower():
        case "y":
            print("")
            return True
        case "n":
            print("Quitting program.")
            return False
        case default:
            print("")
            print("Invalid answer. Please try again")
            askAgain()

def remainingRequests(req):
    print("You got {} out of {} requests left!".format(req.headers["x-ratelimit-remaining"], req.headers["x-ratelimit-limit"]))

def askPostID(post_id):
    if (len(post_id) == 0):
        post_id = input("What's the id of the post? ")
        return post_id
    else:
        wow = input("Do you want to use the [c]urrent ID stored or pick a [n]ew one? ")
        match wow.lower():
            case "c":
                print("")
                return post_id
            case "n":
                post_id = input("What's the id of the post? ")
                return post_id
            case default:
                print("Invalid answer. Please try again")
                askPostID()

def getPostInfo():
    req = requests.get("https://api.imgchest.com/v1/post/{}".format(post_id), headers=auth)
    if (req.ok == True):
        print("Post info get succesful! ", end="")
        remainingRequests(req)
        return req
    else:
        print("Post info get unsuccesful. ", end="")
        remainingRequests(req)
        return ""

def askFolder():
    x = input("What's the path of the folder? ")
    return x.replace("\"", "")

def askTitle():
    x = input("What will be the name of the post! ")
    return x

def getImages():
    imgs = []
    for fle in os.listdir(fol_path):
        if fle.split(".")[1] == "png": f_type = "image/"
        elif  fle.split(".")[1] == "gif": f_type = "gif/"
        with open(fol_path+r"\\"+fle, "rb") as temp:
            imgs.append( ("images[]", (fol_path+fle, io.BytesIO(temp.read()), f_type+fle.split(".")[1])) )
    
    if len(imgs)>20: print("Exceeded image limit, maximum is 20. {} of images couldn't be uploaded succesfully.".format(len(imgs)-20))
    while len(imgs)>20: imgs.pop()
    return imgs

def sendPost():
    body = {"title": post_title, "privacy": "hidden", "anonymous": 0, "nsfw": "false"}
    req = requests.post("https://api.imgchest.com/v1/post",headers=auth, data=body, files=imgs)
    if (req.ok == True):
        print("Post upload succesful! ", end="")
        remainingRequests(req)
        return req
    else:
        print("Post upload unsuccesful. ", end="")
        remainingRequests(req)
        return ""
    
def updatePost():
    req = requests.post("https://api.imgchest.com/v1/post/{}/add".format(post_id),headers=auth, files=imgs)
    if (req.ok == True):
        print("Updated post succesfully! ", end="")
        remainingRequests(req)
        return req
    else:
        print("Post update failed. ", end="")
        remainingRequests(req)
        return ""
    
def deletePost():
    req = requests.delete("https://api.imgchest.com/v1/post/{}".format(post_id),headers=auth)
    if (req.ok == True):
        print("Deleted post succesfully! ", end="")
        remainingRequests(req)
        return req
    else:
        print("Post deletion failed. ", end="")
        remainingRequests(req)
        return ""

#declare variables

post_id = ""
program = True

print("Welcome to imgchest API program!")
auth_code = input("What is your authorization code? ")
auth = {"Authorization": "Bearer {}".format(auth_code)}
while (program == True):
    print("What would you like to do?\n[Create] a new post\n[Post] new pics to an already existing post\n[Delete] a post\n[Exit] the program")
    programCase = input()

    match programCase.lower():
        case "create":
            fol_path = askFolder()
            post_title = askTitle()
            imgs = getImages()
            req = sendPost()
            post_id = json.loads(req.text)["data"]["id"]
            program = askAgain()
        case "post":
            post_id = askPostID(post_id)
            fol_path = askFolder()
            imgs = getImages()
            req = updatePost()
            program = askAgain()
        case "delete":
            post_id = askPostID(post_id)
            req = deletePost()
            program = askAgain()
        case "exit":
            print("Quitting program.")
            program = False
        case default:
            print("Not a valid choice! Please try again\n") 