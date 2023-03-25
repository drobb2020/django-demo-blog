<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/drobb2020/django-demo-blog">
    <img src="static/images/logo.png" alt="Logo" height="120">
  </a>

  <h3 align="center">The New Excession Blog</h3>

  <p align="center">
    This is a blog site to replace a broken blog after upgrading the Linux server on which it was running.
    <br />
    <a href="https://github.com/drobb2020/django-demo-blog/wiki"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="http://blog.excession.org">View Demo</a>
    ·
    <a href="https://github.com/drobb2020/django-demo-blog/issues">Report Bug</a>
    ·
    <a href="https://github.com/drobb2020/django-demo-blog/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

[![Product Name Screen Shot][product-screenshot]](http://blog.excession.org)

This is a Django project using the latest version of Django and bootstrap. It has a nice layout, but all posts must be made from the admin console. I might address this later by adding a post creation and update methods, but for now this will suffice. Since this is behind a firewall and in my private lab entering posts from the admin site is not a big deal for me.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

- [Python](https://python.org)
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

As this project is based on a YouTube Tutorial video series by John Elder of Codemy.com I suggest that you watch the series of [videos](https://www.youtube.com/watch?v=B40bteAMM_M&list=PLCC34OHNcOtr025c1kHSPrnP18YPB-NFi) he created.

### Prerequisites

You will need Python installed on your machine before you start this project. As well you will need a code editor. John Elder is fond on Sublime Text, I personally use Visual Studio Code. Bother work equally well.

### Installation

1. Create a directory on your local filesystem.
2. Change into the directory and create a new virtual environment

   ```sh
   python3 -m venv venv
   ```

3. Clone the repo

   ```sh
   git clone https://github.com/drobb2020/django-demo-blog.git
   ```

4. Install required modules

   ```sh
   pip install -r requirements.txt
   ```

5. Start up the project

   ```sh
   python manage.py runserver
   ```

6. Stop the project

   ```sh
   ctrl+c
   ```

7. Make Migrations

   ```sh
   python manage.py makemigrations && python manage.py migrate
   ```

8. Create a superuser

   ```sh
   python manage.py createsuperuser
   ```

9. Now run the server and start playing

   ```sh
   python manage.py runserver
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Created to learn django and web development I'm using this project to self host a blog site. I will primarily use the site to post technical articles when I find something new and interesting that I want to remember and reuse in other projects.

_For more examples, please refer to the [Documentation](https://github.com/drobb2020/django-demo-blog/wiki)_

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

See the [open issues](https://github.com/drobb2020/django-demo-blog/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

David Robb - [@davidrobb2](https://twitter.com/davidrobb2) - drobb2011@gmail.com

Project Link: [https://github.com/drobb2020/django-demo-blog](https://github.com/drobb2020/django-demo-blog)

Live Link: [http://blog.excession.org](http://blog.excession.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- John Elder & [Codemy.com](https://codemy.com/)
- [YouTube Tutorial](https://www.youtube.com/watch?v=B40bteAMM_M&list=PLCC34OHNcOtr025c1kHSPrnP18YPB-NFi)
- [Choose an Open Source License](https://choosealicense.com)
- [Img Shields](https://shields.io)
- [GitHub Pages](https://pages.github.com)
- [Font Awesome](https://fontawesome.com)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/drobb2020/django-demo-blog.svg?style=for-the-badge
[contributors-url]: https://github.com/drobb2020/django-demo-blog/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/drobb2020/django-demo-blog.svg?style=for-the-badge
[forks-url]: https://github.com/drobb2020/django-demo-blog/network/members
[stars-shield]: https://img.shields.io/github/stars/drobb2020/django-demo-blog.svg?style=for-the-badge
[stars-url]: https://github.com/drobb2020/django-demo-blog/stargazers
[issues-shield]: https://img.shields.io/github/issues/drobb2020/django-demo-blog.svg?style=for-the-badge
[issues-url]: https://github.com/drobb2020/django-demo-blog/issues
[license-shield]: https://img.shields.io/github/license/drobb2020/django-demo-blog.svg?style=for-the-badge
[license-url]: https://github.com/drobb2020/django-demo-blog/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: static/images/screenshot.png
