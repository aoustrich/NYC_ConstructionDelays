## Part 1 - Choose a Topic
- Joe thought the idea was cool and asked if it would be for all construction projects or just certain sizes of projects
	- -> Based on my initial searches for data sets it seemed like it would be projects of all sizes
- Samantha said "This is a great project idea!!"
- Josh asked if I'd get data to compare different cities 
	> I thought it would be cool to do that but it's been harder to process the data than I thought it would be 	> and I don't have time to look at other cities for this assignment. I haven't looked yet, but I imagine it 	> will be hard to make comparisons because different cities will likely track the data differently

## Part 2 - Data Collection and Cleaning - Blog Post 1
> [!NOTE]
> Feedback was given on [this version](https://github.com/aoustrich/aoustrich.github.io/blob/572d585c722800bc4dd248f83c61ef505f6c7351/_posts/2023-11-29-Construction-Delays-Part-1.md) of my post's [markdown file](https://github.com/aoustrich/aoustrich.github.io/blob/master/_posts/2023-11-29-Construction-Delays-Part-1.md)
> SHA Code: 0b1d1ca7a0c0300b8d3b54bb0b0a5c4f2fffd41a

*Aidan (in class)*
- Liked the post and thought it was engaging and well organized. 
- Noticed the formatting for a link was incorrect 

*Michelyn (not in class)*
- Noticed the same link formatting error as Aidan

*Braden (in class)*
- Noticed the link formatting issue
- Noticed that I didn't talk about the budget data


*Changes I made*
- Ficed the link formatting and added more descriptions to the data gathering/cleaning process for the data on the project budgets. These changes made my blog post more readable and consisten with the project. They also made things more professional since the errors were corrected and all parts of the project were discussed. After asking Dr Tass on Discord about the ethical concerns of using an API, I added a section about how I used the API Key and Secret according to the terms of service.

## Part 3 - Exploratory Data Analysis - Blog Post 2
> [!NOTE]
> Feedback was given on [this version]([https://github.com/aoustrich/aoustrich.github.io/blob/572d585c722800bc4dd248f83c61ef505f6c7351/_posts/2023-11-29-Construction-Delays-Part-1.md](https://github.com/aoustrich/aoustrich.github.io/blob/572d585c722800bc4dd248f83c61ef505f6c7351/_posts/2023-12-11-Construction-Delays-Part-2.md)) of my post's [markdown file](https://github.com/aoustrich/aoustrich.github.io/blob/master/_posts/2023-12-11-Construction-Delays-Part-2.md)
> SHA Code: 0b1d1ca7a0c0300b8d3b54bb0b0a5c4f2fffd41a

*Aidan (in class)*
- Liked the consistency in the plot themes
- Noticed typo in text
- Noticed misconfigured HTML code

*Michelyn (not in class)*
- Impressed by the analysis 
- Noticed typo in "69% [of] projects"
- Noticed typo in "but some borough[s]"

*Braden (in class)*
- Liked the limitations section
- Noticed misconfigured HTML code
- Suggested future analysis to compare cities
- Suggested including a main takeaway from each section

*Changes I made*
I corrected the identified typos and even found a few others which improved my blog by making it more professional. I also reformatted the html code for links and tables to make the blog post both more professional and more interactive/informative. I really liked Braden's suggestion to add some takeaways to summarize my findings for each major section of the analysis. The project could seem a bit complicated so this addition really helps solidify my conclusions and makes it easier to read.


## Part 4 Dashboard
> [!NOTE]
> Feedback was given on [this version](https://github.com/aoustrich/NYC_ConstructionDelays/blob/218c189687995abcdcee7c3cdf480fbb4603863b/app.py) of my `app.py` [code](https://github.com/aoustrich/NYC_ConstructionDelays/blob/main/app.py)
> SHA Code: 218c189687995abcdcee7c3cdf480fbb4603863b

*Aidan (in class)*
- Liked the sidebar tab with links to everything
- Liked the expandable sections with plots to make things less cluttered
	- I asked if having it so only one section was open at a time would be good and he said yes

*Michelyn (not in class)*
- noticed the 3 plots in the first section were all the same and that the plot in the final section was always the same despite changing the inputs.

*Braden (in class)*
- Liked the dashboard and suggested I made it so only one dropdown plot was open at a time

*Changes I made*
I fixed the mistakes Michelyn noticed with the plots not changing or being incorrectly labelled. This was a huge mistake so it really improved my dashboard. This was caused by copy/pasting a function to create the plots and not changing all the important labels and parameters for the function and taught me a valuable lesson about having multiple functions that basically do the same thing instead of using one function with changeable arguments. 

The feedback I got about making it so that only one expander section was open at a time was helpful and I looked into using the session state to make this work, but simply did not have enough time to implement these changes during the finals period. I did learn a lot from my research and think there are a few other ways I could use the session state to improve the functionality of my app so it was a worthwhile experience. I will make these changes in the future. 

I also found the reason why my hover text was including a weird extra box with the number 0 in it and found the solution to be including "<extra></extra>" at the end of the custom hover template to specify that the extra info in the hover text was null.