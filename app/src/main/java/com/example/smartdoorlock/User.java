package com.example.smartdoorlock;

public class User {

    public String userName;
    public String userID;
    public String userPW;

    public User() {
        // Default constructor required for calls to DataSnapshot.getValue(User.class)
    }

    public User(String userName, String userID, String userPW) {
       this.userName = userName;
       this.userID = userID;
       this.userPW = userPW;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getUserID() {
        return userID;
    }

    public void setUserID(String userID) {
        this.userID = userID;
    }

    public String getUserPW() {
        return userPW;
    }

    public void setUserPW(String userPW) {
        this.userPW = userPW;
    }



    @Override
    public String toString() {
        return "User{" +
                "userName='" + userName + '\'' +
                ", userID='" + userID + '\'' +
                ", userPW='" + userPW + '\'' +
                '}';
    }
}
