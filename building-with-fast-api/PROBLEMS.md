# Slow 4G

> What are the key areas of concern?

- Client -vs- backend work (E.g: local-first)
- Costs (E.g: running multiple databases)
- Customer job (E.g: this person's job, this time)
- Internet speed (E.g: slow city 4G)
- Packet transfer size (E.g: single -vs- bulk)
- Web obesity problem (E.g: Facebook)

You could replace "events" here with a lot of things: restaurants, hotels, etc.


## What if?

> Finding patterns to create a small language.

What if we looked at [the problem](#the-problem) in a way that narrows down the [actions](#what-actions-are-available) for a hyper-focused [solution](#solution)? What if we built everything around a very particular customer job? Perhaps you pick two:

- User is in a hotel with solid wifi
- User is out on the road in the city

If we thought from 1st principles _only_ for this particular customer job, this time, in this situation, removing everything that isn't needed, how might the solution look?


## The problem

> What is the exact problem?

Take for example, a user looking for an event in a Google Maps style app, for example. How bad is the 4G in that area? The following things might go wrong:

1. Nothing loads
2. Text loads without photos
3. Some photos load per event
4. Everything loads

None of these account for specific user actions, which also may not work, depending on the internet connection. Actions like "add review" or "add to my map" might only work if the internet is up. Which job situations can you guarantee everything will load correctly? Which situations can you not? Which jobs do you serve?


## What actions are available?

1. Read all `/event`s
2. Select one `/event/id`
3. Get a `/event/id` address
4. Get a `/event/id` direction
5. Post a single `/event`
6. And so on ...

Ideally you'd have the minimal amount of actions and data to get a customer job done. Here the main data would be a `.jpg` image of the venue and `json` data for specifics. Let's take one operation, "Read all `/meal`s" as an example.


## Reading all events

> Take into account the customer job AND your vision!

- Customer job: "find a dance music event"
- Internet speed: potentially be bad
- User can view as: list or map
- Radius is: wide or narrow

### Web obesity (too much data)

> Google Maps shows A LOT of data!

Google shows a map regardless of what the user is doing, or what they may want. Is this truly necessary? When you think about it in terms of customer job specifics, and if 4G is your biggest concern, priorities could be vastly different from searching at home with solid WiFi.

Maps does speed up things a lot with vector-based tiles and assets (lines, curves, polygons), by rendering locally on the user's device. For example, they may cache offline results when using the app (-vs- the browser). 

It's still working from the assumption that "maps are good" for every occasion, however. This means large assets sizes, a complex UI, and many search results, are built-in without (seemingly) a critical eye.

To be fair, it's pretty small at 5.43kb for the initial map launch, BUT ...

- **Raises to 715kb** after a search
- **Raises to 2MB** on first event click
- **Raises to 10MB+** if user launches all photos for that event

Multiply that by the average number of events a user might view in one sitting, and we're talking about **_impossible transfer sizes_ on a shitty 4G connection**.


### Customer job specifics

1. 5Ws of this particular job
2. How does it fit into their day?
3. Is it the same or similar to other jobs?
4. And so on ...

### Solution

> Total app speed for 5Ws in this location?
> Reduce it down to 1st principles for the win!<br>

The absolute essentials of this particular job might be:

- Area has very poor connection by mobile internet
- Area has decent connection for cellular service
- Current location within radius of event
- Cuisine style is the main picking criteria
- Customer job must be satisfied right now![^1]

The situation would be _very_ different if the user was at home or in the office with (likely) perfect WiFi connection. Consider the frustration arriving in an area and not being able to reliably search for a place to eat! Consider a customer journey with a poorly operated messaging system that doesn't reliably work![^2]

- What if we already knew the user's likes and dislikes?
- What if we reduced down the search results to an absolute minimum?
- What if we got rid of the maps completely?[^3]
- What if we surprised and delighted the customer?

Well, the solution might look very different:

1. **3 results only** are provided so internet speed no longer matters
2. **Actions for user** ("favourite" etc) **performed with wifi connection** only
3. **Caching is no longer needed** but you can gzip the assets on server
4. **Event phone number** is available for reliable cellular directions
5. **File size is absolutely tiny** with `json` and (optional) 1x `.jpg`[^4]
6. **Location radius narrows down results** even more (10mins walk)
7. **Location directions in text format** are written down for locals
    - Perhaps you don't need directions at all and open Google Maps?
8. **Packet size is small enough** to let backend do all the work
9. **Text-only search** now means website obesity is negligible
10. **Only some events are hosted** such as EDM for a narrow catalogue

What else can you think of? The experience could be hyper-narrowed only for that particular customer job, at that particular point in time. Or perhaps you only cater for that particular job and ignore all others?


## Other considerations

- Does this customer, this time, want this format?[^5]
- How does it fit into their everyday life?
- Is the stack within my skill set?
- Is the vision and purpose clear enough?
- Is there any need at all for a CDN?
- Have you compressed data as much as possible?
- How much does this app cost to run?
- What could go wrong and how likely is it?



[^1]: Is the user needing results in-real-time or are they happy to wait or pre-prepare? Is it "show me an event happening in the next hour" or "which events are happening next week"? Who, exactly, are you catering for?

[^2]: I'm drawing parallels with a shitty automated phone service or Ai bot where you just can't get at the information or person you need without a lot of hassle. It's _artifacts_ again; easier for the business but way worse for the end-user.

[^3]: Maps are very, very, handy for some applications, such as looking for a property to rent, where you'd really want to see the location before contacting the estate agent .. BUT, you're likely viewing that on a better connection. It's not an "immediate" search. You have time to peruse. You need to make an appointment. And so on.
 
[^4]: Perhaps we disable any clickable event view, only display a few images even with wifi connectivity, and stick to a very specific photo style guide (the subject, the formats, etc).

[^5] Hunting for brunch for the girls is very different: maybe we serve this job, and maybe we don't!