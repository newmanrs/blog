---
title: "Jsonresume: Templated Resumes"
date: 2018-03-05T12:42:06-08:00
draft: false
tags:  ["npm", "resume", "json"]
---

[Jsonresume](https://jsonresume.org/schema) is the tool I used to generate the [resume](/resume/resume/) on this site. I am a user&ndash;not author&ndash;of this software.  This tool has a few quirks, but I appreciate concept of separating raw data from its representation whenever possible, and with not having to manually format said representation.

<!--more-->

I suppose it is generally a good to separate data and representations when time permits&mdash;this allows data transfer to new templates for different rendering and layouts, and moreover moves towards the tantalizing dream^[Okay, I may be overhyping this, but I really don't like having to synchronize updates to multiple places.] of maintaining only one set of data that can be used for both a short-form resume and a long-form CV instead of maintaining two separate documents.  Of course, I still have not done so.

# Basic Idea

What jsonresume does is store the contents of a resume by section into an json file (with some schema naming for the keys).  Incase anyone reading this isn't a programmer, it means that the data that is used in the resume is stored entirely separately from the software that renders it: the data is transferred into the template containing the layout.  An example excerpt^[Excerpt chosen by maximal bragging.] of the data is stored in a program-readable format (JSON), which appears similar to as follows:

```json
{
    "education": [{
        "institution": "University of Michigan",
        "area": "Chemical Engineering",
        "studyType": "Doctor of Philosophy",
        "startDate": "2009-09-01",
        "endDate": "2016-07-31",
    }]
}
```

Nonprogrammers may find the brackets in json obnoxious, but it's the price paid to banish most ambiguity.^[Generally, computers do what you say, not what you want.] I probably don't want to know how many hours humanity has spent unmangling CSV files. The file I used to generate my resume is [available here](/json/resume.json).  This information is ingested into jsonresume into some templates which select which data to use and outputs the resume as a [HTML page](/resume/resume/).  The [quickstart guide](https://jsonresume.org/getting-started/) to use this software project is simple.
Briefly, you'll need some kind of unix-like shell which is now available even in Windows. And assuming if the `resume.json` is in the same directory (and that you've installed the node package manager (npm), the basic evocation to install is as follows:

```
npm install jsonresume
```

Then to render as [HTML](/resume/resume/)^["See, in my line of work you got to keep repeating things over and over and over again for the truth to sink in, to kind of catapult the propaganda." - George W. Bush] using the default template:

```
resume export resume.html
```

The provided online documentation for the project is good - there's no need for me to delve deep into them here since they actually provide a complete set of steps^[The reader may consider this either high praise or low expectations.].  Usual flags etc. if you use a different file name or want to select a particular theme.  In my use cases it worked as advertised for generating HTML resumes with nice templates without too much finagling.

# The Ugly

As of the date of this post (and since I first used the tool over a year ago) direct rendering to PDF is broken.  You'll have to use Chrome to print to PDF, and manually edit the HTML as required to do section breaks on most of the templates. The project does acknowledge the PDF is broken and seems to be trying to work towards a solution.

# The Minor

Jsonresume comes with several source templates that are obtained from npm.
These templates, however, can not be run from local (unless this has been changed since last use).  The consequence of this is that you have to fork the repository (create your own copy descendant from) to make even minor edits.  This does does cause a bit of an extra barrier to making changes formatting.^[ I suppose on the other hand being unable to modify templates locally also forces me (and anyone else making changes) to make their work publicly available for other people's use.] It's not hard, but if you hadn't used npm before it makes for another side task and set of steps to learn.  That said, having to commit changes without testing them is obnoxious.  Fortunately, the templates provided aren't too bad, if I recall I believe I only had to change some spaces to non-breaking spaces.

# Last opinions

I feel this tool is more than good enough to generate HTML resumes that look good with minimal effort.  Editing json files by hand without accidently creating invalid files is the hardest step.  I do hope someone finds the time to contribute fixes to direct PDF rendering, although you can always work around this.  The project webpage also seems to be creating a web-based editor that can mitigate this and make adoptation easier.

Even if this isn't the project that survives for constructing resumes from templates, conceptually these templates only need to be written once and can be disseminated so anyone can benefit from others significant design efforts.
Has anyone really ever enjoyed peforming iterations of formatting and layout of resumes manually?
I am glad I can use someone else's layout and design to save myself the time and effort.
And honestly&mdash;they probably have better aesthetic tastes than I do.
