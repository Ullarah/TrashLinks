# Yet another link aggregator project

TrashLinks was designed with a specific audience in mind; myself and a bunch of other weirdos.

This is my first (and hopefully not last) Python + Flask project.  If you're reading this and looking at the code keep in mind that I am not a professional programmer by any means and I do this simply because I like coding and it helps me relax (weird right?).

I have also tried to keep this project as far away as possible from Javascript.  Not that I have anything against it, it was just one of my many goals.  Every website these days are heavy in Javascript usage, let's bring it back down to simpler times.

The project is inspired by the likes of Reddit, Hacker News, Lobsters and another one that I don't wish to mention.  Also, this isn't a social media project.  No text posts, no comments.  Just good ol' fashioned web links, think of it like a public bookmarking site.  That's how I like to think of it.

## Todo

Below are some ideas for the short and longer term. New ideas and push requests welcome! Especially if you're able to fix some of my badly written code and explain to me the changes so I can learn.

- [ ] KISS method of coding (limit the number of requirements)
- [ ] Comment code (Important todo! Future me will be thankful)
- [x] ~~Telegram integration~~
- [x] ~~RSS feeds for global and user subscription~~
- [ ] Simple and fast web app (no javascript)
- [ ] API (maybe? everything has an API these days...)
- [ ] Administration backend
- [ ] Better / faster encryption (takes a while to login)
- [ ] Add option for multiple tags (support is there, just not sure best way to implement)
- [ ] Add some colour to the project
- [ ] Maybe denote deleted posts instead of actually deleting them (garbage collect?)
- [ ] Better search functionality
- [ ] Check for identical titles and URLs
- [ ] Dialog for delete confirmation
- [ ] Top domains (Just like the tag list)
- [ ] Custom tags (Coloured?)
- [ ] 18+ Post marks
- [ ] Moderation queue for posts
- [ ] Hidden posts - Only people who go to your profile can see hidden posts
- [ ] Somehow combine desktop and mobile views together

## Installation

Honestly, I tried my best to make it easy to (re)install.  The database is created with a super user (look in data/config.json) and you use the invite code to create yourself.  The super user does not have any ability to login (unless of course you change this directly in the DB).

Maybe one day I'll edit this document and put in some step-by-step instructions...

## Thanks

I'm just grateful that you're looking at this project and took the time to read it.  This project is in a large sea of other projects that are similar, but this one is mine, and I enjoy coding/using it.  If it's still up and running you can look at an example here, quisquiliae.com
