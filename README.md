# finance-solution

## Background

This is an application to help people understand and manage their finances by aggregating their data and summarizing it through easy-to-understand visuals. This is a work in progress.

## Files

### Client

This is where frontend code lives. It is an Emberjs app.

### Database

This is where the Sqlite3 database lives.

### Server

This is where the server code lives. It is a Flask app that leverages the Plaid api for financial data.

## TODO

This section outlines the steps necessary to finish the app.

- [ ] Create a user database
- [ ] Create a sign up and login flow
- [ ] Allow users to link to multiple financial institutions
- [ ] Store the access link in the database
- [ ] Store the user's financial data in the database
- [ ] Display a table of basic transactions
- [ ] Organize transactions by category

## Future Work

- [ ] Add OAuth for Google login
- [ ] Add a cloud DB solution
- [ ] Create a Makefile
- [ ] Containerize the app via Docker
- [ ] Update this to use React Native and publish in the App Store
