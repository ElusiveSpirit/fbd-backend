# FBD Backend
Feature Branch Deployment backend for merge requests' testings.
> Not complete production app, just to show an example

## Description

Using nginx-proxy to create an auto-refreshing routing system for multiple docker-compose apps in a single network to allow users to access apps via different domains created from branch slug.

Example:  
Developer opens Merge Request with a feature. Team-lead or analyst needs to review it. CI/CD system deploys this app version along with others. So the reviewer could access it via subdomain style link like `http://feature-branch.awesome-app.com`

## Use-cases

* Store and Show deployed branches
* Stop and clean up a branch
* Open public access for a branch by switching access port
