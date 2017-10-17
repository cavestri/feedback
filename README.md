Feedback
--------

**Feedback,** is a small application made with **Flask**, **Jquery** and **SQLite**.

It's divided in two parts:

 - A **REST API** for **POST** and **GET** feedback data.
 - A **UI** to visualize the data

The **ADD** resource allows publish messages that will be stored in the database, by example:

    {
        "name": "Franco",
        "type": "like",
        "comment": "I love the new UI!"
    }

The **GET** resource allows retrieve data filtering by preset filters:

**range:** *today, week, month, all*
**type:** *like, dislike, issue*

The GET resource is used in the UI:

![UI](https://github.com/cavestri/feedback/blob/master/feedback.png)

In the **UI** you will see three big circles, with likes, dislikes and issues information, along with a table with the user, description and date.

**The filters allows you to filter the entire UI by type and range.**

The idea behind **Feedback** is that you can add a feedback button that publish to the APP, allowing your users to sent how they feel with the service that you provides  and valuable comments to improve it.
