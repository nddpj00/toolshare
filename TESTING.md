
### Manual Vs Automated Testing

- I opted to **manually** test my site.  The reasons are -  

    1. As the sole developer I can quickly carry out tests as I go and can obtain immediate results from the test.
    2. As the main purpose of the site is to learn about Full Stack Frameworkds, show understanding and gain a qualification; and won't need to be maintained in the long term, I felt the time it would take to build an automated testing process was unnecessary on this occasion.  In a real-world situation, the use of a test framework, especially Django's in-built testing framework would be invaluable to ensure the continuous integrity of the site.
    3. UX testing. Important to the overall usability of the site and can only be carried out via manual testing. Automated testing lacks human observation and cognitive abilities.

- Reasons why I would use Automated Testing in the future for other projects.

    1. Larger scale site or application that may have an increased amount of functionality and code. Manual testing would take too long.
    2. Working in a team. Possibly no one person with in-depth knowledge of how the whole site should work and perform. Automated tests would allow anyone to run them.
    3. Continual code added to the site. Automated tests can be run after every addition, ensuring no disruption to the existing code.
    4. Higher accuracy. Important if the site is in the public domain and linked to an organization. To avoid deprecation of the 'brand' due to a poor website.
    5. Time. Though they take longer to set up initially, having a bespoke automated testing process will save time in the long run, due to how frequently they need to be run when maintaining and improving the site.


### Manual Test process  

  - The Test
## Home App
1. All navbar links work.
1. Latest Blogs and Event links work and take you to correct page.
1. Search bar works, filtering the categories and items.
1. Links for social media work.
1. Links to email and phone open respective client programmes.

## Items App
1. Item list
1. Filtering of items by Category.
1. Sorting of items. Price, Name, Category
1. Links to item details.
1. Edit and Delete works render and work for staff only

2. Item Details
1. Edit and Delete works render and work for staff only.
2. Keep Shopping and Add to Bag button work as intended.
3. Decrement button doesnt go below 1.
4. Increment button is disabled when stock quantity met.
5. Toast/messages show correct information depending on the action.
6. Bag total updated with quantity x price amount.

### Outcomes

<img align = "center" width = "500px" height = "350px" src = "mealplanner/static/images/testing/manual-testing-matrix.png"> 

I used a programme called BrowserStack to perform the tests. This is software provided as part of the course, included in the Student Developer pack.  This software allows you to load your site on a live environment on each device and browser.

The application recommended that 1 x high-end, 1 x low-end device and a tablet is tested for each main manufacturer of smart devices.  I tested Apple,Samsung and Google devices of differing size.  

Also, I've tested the site on a broad cross-section of browsers.  Chrome, Edge, Safari, Firefox and Opera.

The site performed well across all devices and browsers. All links worked as expected.  Appearance and layout looked good on all devices too.


A small selection of screenshots showing the cross-browser testing.  
Windows 11  
<img align = "center" width = "200px" height = "100px" src = "mealplanner/static/images/testing/bdrf-testing-windows11.png">   
Mac Big Sur 14.1  
<img align = "center" width = "200px" height = "100px" src = "mealplanner/static/images/testing/bdrf-testing-mac-bigsur-14.1.png">   
Apple Iphone 14  
<img align = "center" width = "100px" height = "200px" src = "mealplanner/static/images/testing/bdrf-testing-iphone14.png">  
Samsung S21 Ultra  
<img align = "center" width = "100px" height = "200px" src = "mealplanner/static/images/testing/bdrf-testing-s21ultra.png">  
Apple Iphone SE 2022   
<img align = "center" width = "80px" height = "150px" src = "mealplanner/static/images/testing/bdrf-testing-iphonese-small.png">  
Apple iPad Pro 11  
<img align = "center" width = "150px" height = "200px" src = "mealplanner/static/images/testing/bdrf-testing-ipadpro11-2021.png">  

---
## **BUGS** ##
1. If a user incorrectly input 60mins or over in the minute field for the cook time a DataError was produced.
    <img align = "center" width = "200px" height = "100px" src = "mealplanner/static/images/testing/bdrf-bug-over60mins.png">
1. When editing a recipe the cook time wasn't pre-populating, remaining empty.
1. If user clicks on 'Get random recipe' button, though it worked, the variable stored the recipe.  Meaning if the user clicked it over & over again it would show the same recipe. 
1.  When deploying my original app I ran in to a problem with the database.  It wasn't creating the database and linking to the app.  After many hours trying to resolve I decided to copy the code on to a new workspace and re-attempted the deployment.  Unfortunately my 'commits' will be linked to that original Repo ["mealplanner.2"](https://github.com/nddpj00/mealplanner.2)

## Fixes
1. The dataerror was due to using the incorrect datatype I believe.  In the form I changed the type to "time" and this resolved it immediately.
1. The data stored in the database was in the incorrect format.  By added 0 before the value on the html resolved this. ie value="0{{ recipe.cook_time }}" .
1. I added some Javascript to reload the page on the 'close' button to allow a new recipe to be set as random.
1. New workspace is this one and the deployment was successful.


### Known Bugs
No known bugs
