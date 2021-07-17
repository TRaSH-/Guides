# Release Profile RegEx (WEB-DL)

!!! danger "Advanced feature"
    The regex isn't mentioned anywhere, it's a hidden advanced feature

Sonarr V3 has a great feature called Release Profile.
With this option you can fine tune your preference.

The Release profile that we're going to use for this example is mainly to prefer P2P releases over Scene releases, (Scene releases are still being downloaded but upgraded).

!!! question ""
    **If you don't care about quality then stop reading and see if the other tutorials are helpful for you.**

??? question "FAQ"

    ## FAQ

    **Q: Why do you only have a release profile for WEB-DL?**

    A: I only do WEB-DL my self for TV shows because in my opinion WEB-DL is the sweet spot between Quality and Size and you often don't see big difference anyway for TV shows. (Except for shows like GOT, Vikings, etc)

    **Q: Why do you prefer P2P groups over scene releases?**

    A: Scene release always release in a rush to bring it out as fast as possible.

    So I noticed  often that I got Repacks/Proper releases from them or from different groups and quality.
    P2P releases are a bit smarter and work sort of together by not doing the same release.
    Also I noticed that with some Scene releases the 5.1 audio was stripped out or converted to AAC audio.
    And in my opinion the P2P are of better quality.
    Theirs 1 Scene releaser that do bring out quality releases `-deflate/-inflate`.

    **Q: Why do I see that many Amazon WEB-DL's repacks/proper lately?**

    A: A large portion of Amazon WEB-DLs in the last week have only had 192Kbps DD+5.1, because that's all Amazon made available initially.
    The proper 640Kbps DD+5.1 audio might appear a few hours later or a few months, but when they get updated the episodes will be REPACKED.

    **Q: Why did you remove all the scene groups?**

    A: I decided to redo the Release Profile to make it easier for me and the end user to update/manage the Release Profile, I decided not to add the scene groups anymore (and also removing the current ones). Why ? Lately I noticed a lot of popup scene releases meaning we need to update often.

    With this it also means all scene and (yet) unknown groups will be getting a score of `0` and not `-50`.

    I will still keep a eye on them and add the Low Quality Groups to the `-100` score and when I find a new P2P group I will add them, resulting in less updates and a more accurate upgrade.

------

## Propers and Repacks

First we're need to make sure a P2P release isn't being replaced by a Scene Repack/Proper release !

![!rp-settings-media-management-proper](images/rp-settings-media-management-proper.png)

Settings => `Media Management`
Where we going to set it to `Do not Prefer`

Then we navigate in Sonarr to the Settings =>  `Profiles`

![!rp-settings-profiles](images/rp-settings-profiles.png)

Then you will get a popup screen that will look like this:

![!rp-release-profile](images/rp-release-profile.png)

`Must Contain` => add words that the release name **MUST HAVE!**

`Must Not Contain` => add words that the release name **MUST NOT HAVE AND SO TO BE IGNORE!**

`Preferred` => add words you prefer with a certain score what you prefer more or upgrade.

`Include Preferred when Renaming` => When you add `{Preferred Words}` to your renaming scheme it will add this info.

`Indexers` => Specify what indexer the profile applies to.

`Tags` => create a tag so this is only used by shows that you give this tag or else it's global.

The Number between the **[**brackets**]** are the scores the release name will get during a automatic and manual search and with the use of the scores some releases will be preferred over others and even upgraded.

## First Release Profile

!!! important
    We're going to make use of 2 separate release profiles.

--8<-- "docs/Sonarr/generated/streaming.mdt"

??? success "example"

    !!! attention
        These screenshots are just examples to show you how it should look and where you need to place the data that you need to add, they aren't a 100% reflection of the actual data and not always 100% up to date with the actual data you need to add.

        - Always follow the data described in the guide (with the copy paste/option at the end).
        - If you got any questions or aren't sure just click the chat badge to join the Discord Channel where you can ask your questions directly.

        [![Discord chat](https://img.shields.io/discord/492590071455940612?style=for-the-badge&color=4051B5&logo=discord)](https://trash-guides.info/discord){:target="_blank" rel="noopener noreferrer"}

    ![!rp-release-sources](images/rp-release-sources.png)

------

## Second Release Profile

--8<-- "docs/Sonarr/generated/golden-rule.mdt"

??? success "example"

    ![!rp-release-sources](images/rp-golden-rule.png)

??? info "Why the Must Not Contain entry"

    So why did I put `/(?=(1080|720)).*((x|h)[ ._-]?265|hevc)/i` as `Must Not Contain` and what does it do ?

    It blocks/ignores 720/1080p releases that are encoded in x265, why ?

    !!! quote
        x265 is good for for 4k stuff or 1080p if they used the the remuxes as source.
        If the media isn't source quality/remux, then there will be a loss of quality every time.
        Also, once you go x265, typically that file is done.
        It can't be changed to something else without a huge loss of quality.

        Something like 95% of video files are x264 and have much better direct play support.
        If you have more than a couple users,
        you will notice much more transcoding.
        Just depends on your priorities.

        So basically if you are storage poor and just need to save space, use x265.
        The catch is if you want best quality x265, you need source quality files, so you still have huge file sizes.
        If you want maximum compatibility and the option to change your files to something else later,
        then x264.
        It's all really dependent on specific situations for different people

    It's a shame that most x265 groups microsize the releases or use the x264 as source what results in low quality releases. And the few groups that do use the correct source suffer from it.

    That's why  I created my own golden rule.

    - 720/1080p => x264
    - 2160p/4k => x265

------

--8<-- "docs/Sonarr/generated/p2p.mdt"

??? success "example"

    !!! attention
        These screenshots are just examples to show you how it should look and where you need to place the data that you need to add, they aren't a 100% reflection of the actual data and not always 100% up to date with the actual data you need to add.

        - Always follow the data described in the guide (with the copy paste/option at the end).
        - If you got any questions or aren't sure just click the chat badge to join the Discord Channel where you can ask your questions directly.

        [![Discord chat](https://img.shields.io/discord/492590071455940612?style=for-the-badge&color=4051B5&logo=discord)](https://trash-guides.info/discord){:target="_blank" rel="noopener noreferrer"}

    ![!rp-p2p-groups](images/rp-p2p-groups.png)

------

--8<-- "docs/Sonarr/generated/low-quality.mdt"

??? success "example"

    !!! attention
        These screenshots are just examples to show you how it should look and where you need to place the data that you need to add, they aren't a 100% reflection of the actual data and not always 100% up to date with the actual data you need to add.

        - Always follow the data described in the guide (with the copy paste/option at the end).
        - If you got any questions or aren't sure just click the chat badge to join the Discord Channel where you can ask your questions directly.

        [![Discord chat](https://img.shields.io/discord/492590071455940612?style=for-the-badge&color=4051B5&logo=discord)](https://trash-guides.info/discord){:target="_blank" rel="noopener noreferrer"}

    ![!rp-lq-groups](images/rp-lq-groups.png)

------

### Optional preferred preferences

!!! note
    These options are optional and only needed if you got a certain use case for it,

#### Optional HDR - if you prefer HDR

Add this to your `Preferred (3)` with a score of [10]

```bash
/\bHDR(\b|\d)/i
```

#### Optional (use these only if you dislike renamed and retagged releases)

Add this to your `Preferred (3)` with a score of [-25]

```bash
/(\[rartv\]|\[rarbg\]|\[eztv\]|\[TGx\])/i
```

```bash
/(-4P|-4Planet|-AsRequested|-BUYMORE)\b/i
```

```bash
/(-Chamele0n|-GEROV|-iNC0GNiTO|-NZBGeek)\b/i
```

```bash
/(-Obfuscated|-postbot|-Rakuv|-Scrambled)\b/i
```

```bash
/(-WhiteRev|-xpost|-WRTEAM|-CAPTCHA)\b/i
```

#### Optional (matches releases that ends with EN)

Add this to your `Preferred (3)` with a score of [-25]

```bash
/\s?\ben\b$/i
```

#### Optional Matches any release that contains '1-' as prefix for Release Groups

Add this to your `Preferred (3)` with a score of [-25]

```bash
/(1-.+)$/i
```

#### Optional Matches Season Packs (use this if you prefer Season packs)

Add this to your `Preferred (3)` with a score of [15]

```bash
/\bS\d+\b(?!E\d+\b)/i
```

##### .su season pack issue

??? bug ".su season pack issue"

    When you see a error in Sonarr that looks somehow like the follow screenshot

    ![!rp-su-season](images/rp-su-season.png)

    Then theirs only one way real way that always solves this issue.
    create a new release profile specific for .su that uses the [Season regex](#optional-matches-season-packs-use-this-if-you-prefer-season-packs) as `Must not contain (2)`

    ![!rp-release-profile-block-season-su](images/rp-release-profile-block-season-su.png)

    !!! note
        Theirs a [script](/NZBGet/scripts/#wtfnzb-renamer){:target="_blank" rel="noopener noreferrer"} for NZBGet that sometimes could help but it seems it doesn't always work. It also seems theirs a work around for SABnzbd but i can't confirm being i'm not using Sab.

#### Optional Ignore DoVi for WEBDL

??? NOTE "WHY ?"

    This is a RegEx that ignores DV for WEB-DL but allows for other sources. WEB-DL from Streaming Services don't have the fallback to HDR(10), What can results in weird playback issues like weird colors if you want to play it on a not DoVi compatible setup. Remuxes and Bluray have a fallback to HDR(10).

Add this to your `Must not contain (2)`

```bash
/\b(dv|dovi|dolby[ .]vision)\b.*(?=[ ._-]web[ ._-]?(dl|rip)\b)/i,
/(?=[ ._-]web[ ._-]?(dl|rip)\b).*\b(dv|dovi|dolby[ .]vision)\b/i
```

------

### A little explanation of the scores and why

- Scores [75]-[100] Release Source.
- Scores [125]-[150] P2P Groups.
- Scores [10] Give a repack/proper a higher score but don't trump P2P groups for a Scene fix.
- Scores [-25] Retagged/Renames/Obfuscated  releases.

!!! danger "Watch out"
    If you're getting often a error message like `Has the same filesize as existing file`, you might need to consider to remove the [-25]

- Scores [-100] Groups that mess with the audio or add another preferred language.

Optional => We've tested it and it worked for what we've tested it on, if it will work in your situation we don't know if you notice something wrong just contact me and we will try to fix it or remove it.

The reason why I got multiple entry's with the same score is because the line will go out of the box and I don't like how that looks.

## Final Results

When you've done it correctly it will look something like this.

??? success "example"

    !!! attention
        These screenshots are just examples to show you how it should look and where you need to place the data that you need to add, they aren't a 100% reflection of the actual data and not always 100% up to date with the actual data you need to add.

        - Always follow the data described in the guide (with the copy paste/option at the end).
        - If you got any questions or aren't sure just click the chat badge to join the Discord Channel where you can ask your questions directly.

        [![Discord chat](https://img.shields.io/discord/492590071455940612?style=for-the-badge&color=4051B5&logo=discord)](https://trash-guides.info/discord){:target="_blank" rel="noopener noreferrer"}

    ![!rp-groups](images/rp-groups.png)

    And after you clicked on `Save` it will look something like this:

    ![!rp-profiles](images/rp-profiles.png)

------

This list is made by collecting information from Sonarr Discord Channel, and personal testing and a few others that helped.

So I want to thnx everyone who helped to make this list possible, for privacy reasons I decided not to add the names/nick of the persons.

If you want to be mentioned please message me on discord, including a link for proof to what part you want to be credited.

!!! info

    Keep in mind this list will be a constant work in progress because I will be updating it when it's needed.

    So best to set a notification for updates for this page.
------
