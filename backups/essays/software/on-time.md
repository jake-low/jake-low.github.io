---
date: 2016-07-16T00:00:00Z
excerpt: |
  Or, how a simple question about representing times ultimately cost me my sanity.
license: CC BY 4.0
title: On Time
---

This article began as a deceptively simple question.

In a certain networked filesystem, a Java client program retrieves the current time in milliseconds from the local OS clock by calling `System.currentTimeMillis()` and sends it to a server as an eight-byte signed integer. The server is expected to record the provided time as the modification timestamp on a file. The server's filesystem stores times as an `int64_t` for seconds and a `uint32_t` for nanoseconds on inodes.

In the server, what conversion procedure should be used?

## Before you go further

> "It is absolutely necessary, for the peace and safety of mankind, that some of earth’s dark, dead corners and unplumbed depths be let alone; lest sleeping abnormalities wake to resurgent life, and blasphemously surviving nightmares squirm and splash out of their black lairs to newer and wider conquests."
>
> --- H.P. Lovecraft, _At the Mountains of Madness_

You've been warned.

## What is time?

Before proceeding to examine the question in more depth, we need to get a good picture of what time actually is, and more specifically how it's measured or counted.

### How we measure time

There are two different types of time that you deal with in your daily life. One is _absolute time_, which defines a precise moment. The other is _relative time_, which defines a duration. We can combine these two concepts to quantify more complex timekeeping concepts, such as a period in history or an interval on your calendar.

Relative time is actually a measure of the distance between two events along one axis (the time axis) of spacetime. Like mass or energy, we have to define relative time by referring to some physical phenomenon. The units just let us compare a time we've measured to a well-known standard. _"Is it longer or shorter than a second?"_ is the chronometric equivalent to 20 Questions' _"Is it smaller or larger than a breadbox?"_.

Historically, humans have used various natural phenomena as the measuring stick for time. The period of the Earth's revolution and the period of its orbit have both been used in nearly all human cultures (even before the nature of these cosmic events was well understood) because these cycles were important to early humans. They remain important today, and consequently concepts of a _day_ and a _year_ are practically universal.

In order to define absolute time, one must choose a well-known moment in time as the _epoch_. Adding or subtracting a relative time from this epoch results in another absolute time. Moments in time can be thought of as points on a line which are defined by their distance from an epoch, much like numbers can be thought of as points on a line, defined by their distance from zero.

Unlike relative time, which has for all of human history been defined in terms of just a few common natural phenomena, absolute time has been  repeatedly redefined in terms of diffent epochs. Most premodern cultures had their own notion of what historical or (predicted) future event should be used for "zero". Today, most of the world has standardized their definition around an epoch of the first day of the year in which Christ is believed to have been born, though it should be noted that many alternate calendars are still used in certain national, religious, and cultural contexts.

### How computers measure time

Computers, like humans (unsurprising considering their origin), measure time by counting units of relative time since a chosen epoch.

For historical reasons, most computer systems use epochs more recent than the one used by humans. This is because it is (a) desirable to represent absolute times in resolutions of one second or higher, (b) relatively uncommon to need to programatically represent absolute times in the distant past, and (c) the number of bits required to store absolute times near the current time rises if the epoch is set in the distant past.

As a result, epochs for 20th-century computer systems were generally chosen to be dates that were also in the 20th century. Common Lisp and the Network Time Protocol both use January 1st, 1900 as their epoch. POSIX systems use January 1st, 1970 as theirs (the first Unix implementation was released on November 3, 1971). Microsoft Excel chose the rather bizarre epoch of January 0, 1900.

### What is a calendar?

It would be cumbersome to refer to moments in time in seconds since the epoch, because seconds are so short. Human short-term memory operates better on small numbers.

A calendar is a mapping of a set of names onto consecutive spans of time, with each name occurring at a regular period. This allows us to refer to particular moments relative to _other nearby moments_ rather than to the epoch.

For example, the notion that a day is divided into _hours_ (and hours into _minutes_), instead of merely into seconds allows us to refer to a moment in a particular day as `11:17:29 AM`, meaning "29 seconds after the moment that was 17 minutes after the moment that was 11 hours after the first moment of the day". Similarly, the notion that time since the epoch can be divided into _years_ and each year into _months_ lets us understand a moment in the recent past as "December 12, 2005" rather than as a few-hundred-billion seconds since the Christian epoch.

### Theory vs. practice

Calendars are essential in letting humans reason about time. There are simply too many moments in human history to keep track of with raw numbers.

But calendars also have a problem. They are cosmically meaningless. A calendar is a human construct, but the stars and planets don't move according to human schedules. As a result, any _rigid_ calendar system will eventually drift out of alignment with the natural phenomena that humans care about tracking.

### Hail Caesar

The earliest Roman calendar was a lunisolar calendar, meaning it defined a year as twelve lunar orbits. The moon orbits the Earth a little faster than twelve times per solar year (twelve lunar months is about 355 days, but the Earth's solar orbit takes about 365.2425 days), which meant that over time the calendar would get out of alignment with the solar year. The moon would be full on the same day every month, but the summer solstice (the day of the year with the most daylight) would occur later and later with each passing year.

To correct for this, Roman officials were expected to occasionally add an entire extra month (called an _intercalary month_) to the year. In order to keep the summer solstice from moving, this would need to happen about every 33 months, or a bit more frequently than every third year.

However, during the political turmoil of [Second Punic War][second-punic-war] and the [Civil Wars][civil-wars], the necessary intercalations were not performed. When Julius Caesar came to power in Rome in 49 B.C. the calendar was a whopping _ninety days_ offset from the solar year. After consulting with the astronomer [Sosigenes][sosigenes], Caesar introduced a reformed Roman calendar in 46 B.C. which realigned the year with the solar orbit and which did away with intercalary months. Instead, the year was composed of twelve months of fixed length (each greater in length than a lunar orbit), totaling 365 days. To account for the roughly one day of drift that would occur every fourth year, an additional day was added to the calends of March (what is now February) every four years, bringing the length of the mean calendar year to 364.25 days.

It took 1600 years before enough error accumulated in Caesar's calendar that it needed to be reformed again. In 1582, Pope Gregory XIII proposed an alteration to the Julian calendar that would make every centennial year a common year (instead of a leap year), excluding centennial years that are divisible by 400. This brings the length of the mean calendar year to 365.2425 days. The Gregorian calendar is still in wide use today.

### Seconds

The first division of the solar day into units resembling seconds was devised by Muslim scholars in the 11th century. Their notion that a second was the 86400th fraction of a mean solar day was accurate enough for widespread scientific use for over 900 years.

However, the Earth's rotational period varies subtly but unpredictably, making this definition unsuitable for precise measurements. In the 1950s, the International Astronomical Union redefined the second as a fraction of the solar year. [^sidereal-tropical]

Before long this definition too was deemed inadequate, and the second was redefined in terms of a multiple of the duration between two hyperfine ground states of a caesium-133 atom. These state changes take an extremely predictable amount of time, and emit radiation which is easy to detect. This means anyone with a lump of caesium-133 and a detector can determine when precisely one SI second has passed.

### Two notions of time

This leaves us with a definition of the second (known as the SI second) which is unwavering and (relatively) easy to reproduce experimentally. However, it also leaves us with a problem: a solar day is not exactly 86400 seconds.

Competing interests meant that this problem was solved two ways. Some situations call for a clock that ticks in predictable, uniform increments, while others call for a clock that tracks the observed solar time on Earth.

#### Terrestrial Time
To address the former need, Terrestrial Time was established.[^ephemeris-time] TT is a theoretical, idealized timescale. It ticks in SI seconds and pays no regard to the motion of the Earth or the Sun. As a result, it is infinitely predictable into the future, but if you use it to set your wall clock then over time it will drift out of sync from natural phenomena like the sunrise or the vernal equinox.

To approximate TT, a new coordinated time standard was created called TAI. TAI is defined by the average measured time of numerous atomic clocks around the world. TAI has become the backbone of nearly all timekeeping,[^gps] with other notions of time being based on adjustments to the broadcast value of TAI.

#### Universal Time

Addressing the latter need proved to be complex. Another theoretical timescale was devised, called Universal Time. UT was designed to measure the exact solar time, as if the Earth were being used as a huge sundial with infinite precision. One UT day corresponds to one revolution of the Earth with respect to the heavens. UT does not define its days in terms of SI seconds; each UT day has _approximately_ 86400 seconds in it, but the precise number varies and can only be determined by measurement.

Several time systems exist to approximate UT. The most common in use today is UT1, which measures the mean solar day not relative to the sun (as it is difficult to accurately measure the position of a big, bright object like the sun) but relative to extremely distant quasars.

#### UTC

Since UT is an unachievable idealized time, and UT1 (though a very good approximation) can only be determined by measurement, a compromise solution was needed that would track the solar day with reasonably high accuracy, but also be predictable and easy to calculate.

UTC, or Coordinated Universal Time,[^utc-name] was devised for this purpose. The idea of UTC is to tick in seconds of predictable length, but to insert occasional adjustments in order to correct for the skew that occurs between the resulting clock and idealized UT.

It took the international community a while to get the details right on this. In the 1960s, a complicated definition was used with non-SI seconds that were occasionally adjusted in length to correct for skew. This proved difficult to implement, and so the computing community ignored UTC and used TAI as an (arguably poor) approximation.

In 1972, UTC was redefined to tick in SI seconds. To correct for skew between UTC and UT, _leap seconds_ are scheduled by the IERS. A leap second is either an additional SI second at the end of a UTC day (displayed on UTC-aware clocks as `23:59:60`) or the removal of the last second (`23:59:59`) of a UTC day. At the time of writing, 36 leap seconds have been scheduled since 1972, all positive (i.e. insertions) and all on either June 30th or December 31st.

## So what's the big deal?

Let's look at the exact definitions of POSIX time and Java time, and see if we can figure out how to convert between them.

### POSIX time

POSIX time is defined as the number of seconds elapsed since January 1, 1970 at midnight UTC, _not counting leap seconds_. POSIX time assumes all days contain exactly 86400 seconds.

> The relationship between the actual time of day and the current value for seconds since the Epoch is unspecified.
>
> --- <cite>[The Open Group Base Specifications Issue 7](open-group-7), §4.15</cite>

### Java time

Java defines its own timescale, the _Java Time-Scale_, which

---

"Alright, I get it, computers count from different zero points. Can't we just subtract or something?"

Great question. Let's try!

Suppose I asked you to tell me what day of the week July 20, 1969 fell on. How would you figure it out?

"Well, I'd take that date, and subtract it from today's date, and then take the difference modulo 7, and use that to count backwards from the day of the week that's today, and once I did that I'd know what day of the week July 20, 1969 was."

Sounds like a plan! Here, I'll set you up to subtract

~~~c
struct timespec java_to_unix_time(int64_t java_milliseconds) {
    struct timespec result = {
      .tv_sec = java_milliseconds / 1000,
      .tv_nsec = (java_milliseconds % 1000) * 1000 * 1000
    };
    return result;
}
~~~

[^sidereal-tropical]: First relative to the [sidereal year](https://en.wikipedia.org/wiki/Sidereal_year), and soon after redefined relative to the [tropical year](https://en.wikipedia.org/wiki/Tropical_year) as measured in 1900 A.D.
[^ephemeris-time]: Terrestrial Time was actually preceded by Ephemeris Time, which predates the invention of caesium clocks by a few years. As such, ET was based on the _ephemeris second_, taken to be the length of the _tropical year_ of 1900 A.D., divided by 365 days and again by 86400 seconds. When the SI second was defined, care was taken to make it equal to the ephemeris second (though the SI second's length is known to much higher precision).
[^gps]: FIXME GPS satellites do not use TAI, because they broadcast at a rate that is intentionally skewed to counteract for relativity (so client devices don't have to).
[^utc-name]: The French wanted TUC, for _Temps Universel Coordonné_, and the Americans wanted CUT, because the Navy had been calling it _Coordinated Universal Time_. The compromise was UTC, which conforms to the other UT-tracking timescales (UT0, UT1, etc.).

*[TAI]: Temps Atomique International (International Atomic Time)

*[IERS]: International Earth Rotation and Reference Systems Service

[open-group-7]:  http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap04.html

[second-punic-war]: https://en.wikipedia.org/wiki/Second_Punic_War
[civil-wars]: https://en.wikipedia.org/wiki/Roman_civil_wars
[sosigenes]: https://en.wikipedia.org/wiki/Sosigenes_of_Alexandria
