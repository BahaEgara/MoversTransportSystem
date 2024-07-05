<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Welcome to AgriTrans</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" />

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/4.6.1/css/bootstrap.min.css" />
  <link rel="stylesheet" href="homepage.css" />
  <!-- <link rel="stylesheet" href="preload.css" /> -->





  <div class="preload" data-preaload>
    <div class="circle"></div>
    <p class="text">AgriTrans</p>
  </div>
  <style>
    .client1,
    .client2,
    .client3 {
      width: 100px;
      height: 100px;
      background-size: cover;
      /* Adjust the background size to cover the container */
      background-repeat: no-repeat;
      background-position: center center;
      border-radius: 50%;
      margin: auto;
    }

    .client1 {
      background-image: url(images/client1.jpg);
    }

    .client2 {
      background-image: url(images/client2.jpg);
    }

    .client3 {
      background-image: url(images/client3.jpg);
    }

    .reviews .box-container {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      Three columns gap: 2rem;
    }

    .reviews .box {
      background-color: white;
      text-align: center;
      border-radius: 3rem;
      box-shadow: var(--box-shadow);
      < !-- padding: 2rem;
      -->margin: 1rem 0;
    }

    .process .box-container .box img {
      height: 20rem;
      margin: 1rem 0;
      width: 100%;
    }
  </style>
</head>

<body>
  <header class="header fixed-top">
    <div class="container">
      <div class="row align-items-center justify-content-between">
        <a href="#home" class="logo">Agri<span>Trans</span></a>
        <nav class="nav">
          <a href="#home">Home</a>
          <a href="#about">About</a>
          <a href="#services">Services</a>
          <a href="#reviews">Reviews</a>
          <a href="#contact">Contact</a>
        </nav>
        <div class="right">
          <a href="userlogin.php" class="btn">Login</a>
          <div id="menu-btn" class="fas fa-bars"> </div>
          <a href="user_signup.php" class="btn">Sign Up</a>
          <!-- put the sign up home page here -->
        </div>
      </div>
    </div>
  </header>

  <section class="home" id="home">
    <div class="container">
      <div class="row min-vh-100 align-items-center">
        <div class="content text-center text-md-left">
          <h3> Experience Seamless Transport</h3>
          <p>Experience the future of transportation with our state-of-the-art
            system. Whether commuting, traveling across the city, or planning
            a long-distance trip, our innovative technology ensures smooth,
            fast, and enjoyable journeys. Trust us for reliable, efficient,
            and eco-friendly travel. Your journey, reimagined.</p>

          <a href="user_signup.html" class="link-btn">Sign Up!</a>


        </div>

      </div>
    </div>
  </section>
  <!-- home section ends -->

  <!-- about section stats -->
  <section class="about" id="about">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-6 image">
          <img src="images/IMG_5598.JPG" class="w-100 mb-5 mb-mb-0">
        </div>
        <div class="col-md-6 content">
          <span>About Us</span>
          <h3> Where every Journey tells a story
          </h3>
          <p> We pride ourselves on offering a comprehensive range of services
            that ensure timely and safe delivery of fresh produce,
            livestock, fertilizers, machinery, and other essential farm
            inputs. With a focus on innovation, sustainability, and customer
            satisfaction, AgriTrans is committed to supporting the
            agricultural community by providing hassle-free and
            cost-effective transportation solutions.</p>
          <a href="#contact" class="link-btn">Talk to us</a>
        </div>
      </div>
    </div>
  </section>
  <!-- about section ends -->




  <!-- services section start -->
  <section class="services" id="services">
    <h1 class="heading">Our Services</h1>
    <div class="box-container container">
      <div class="box">
        <img src="images/process1.jpg">
        <h3>Order Management Services</h3>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

      </div>
      <div class="box">
        <img src="images/process2.jpg">
        <h3>Market Information Services</h3>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

      </div>
      <div class="box">
        <img src="images/process3.jpg">
        <h3>Logistics and Route Optimization Services:</h3>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

      </div>
      <div class="box">
        <img src="images/process4.jpg">
        <h3>Administrative Services:</h3>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

      </div>
      <div class="box">
        <img src="images/process5.jpg">
        <h3>Support and Helpdesk Services:</h3>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

      </div>
      <div class="box">
        <img src="images/process6.jpg">
        <h3>Performance and Feedback Services</h3>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

      </div>
    </div>
    </div>

  </section>

  <!-- services section end -->

  <!-- process section starts -->
  <section class="process">
    <h1 class="heading">Work Process</h1>
    <div class="box-container container">
      <div class="box">
        <img src="images/workprogress1.webp" alt="">
        <h3>workprogress1</h3>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

      </div>

      <div class="box">
        <img src="" alt="">
        <h3>workprogress2</h3>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>
      </div>


      <div class="box">
        <img src="" alt="">
        <h3>workprogress3</h3>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

      </div>

    </div>
  </section>
  <!-- process section ends -->


  <!-- Reviews start here -->
  <section class="reviews" id="reviews">
    <h1 class="heading">satisfied clients</h1>
    <div class="box-container container">
      <div class="box">
        <div class="client1">
        </div>

        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

        <div class="stars">
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star-half-alt"></i>
        </div>
        <h3>Sarah Kui</h3>
        <span>satisfied client</span>
      </div>



      <div class="box">
        <div class="client2">
        </div>
        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>

        <div class="stars">
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star-half-alt"></i>
        </div>
        <h3>John Doe</h3>
        <span>Satisfied Client</span>
      </div>

      <div class="box">
        <div class="client3">
        </div>

        <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Similique voluptatum quo omnis rem odit sequi
          maxime recusandae, exercitationem corrupti ducimus soluta. Accusantium alias soluta sit quisquam adipisci,
          vitae nemo veniam!</p>
        <div class="stars">
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star-half-alt"></i>
        </div>
        <h3>Victorial Manola</h3>
        <span>satisfied client</span>
      </div>
    </div>
  </section>
  <!-- contact section starts -->
  <section class="contact" id="contact">
    <h1 class="heading">make appointment</h1>
  </section>


  <!-- contact section ends -->

  <!-- footer section starts -->
  <section class="footer">
    <div class="box-container container">
      <div class="box">
        <i class="fas fa-phone"></i>
        <h3>Phone Number</h3>
        <p>0799-545-548->Front desk line</p>
        <p>0723-345-678->Secondary line</p>
      </div>

      <div class="box">
        <i class="fas fa-map-marker-alt"></i>
        <h3>Our Addresses</h3>
        <p>Haile Selassie Road Nairobi, Kenya</p>
        <p>Delamere Naivasha, Kenya</p>
      </div>



      <div class="box">
        <i class="fas fa-clock"></i>
        <h3>Opening Hours</h3>
        <p>07:00hrs-18:00hrs on weekdays</p>
        <p>08:00hrs-16:00hrs on weekends and public holidays</p>
      </div>

      <div class="box">
        <i class="fas fa-envelope"></i>
        <h3>Email Address</h3>
        <p>agriTrans@gmail.com</p>
        <p>agriTrans@yahoo.com</p>
      </div>
    </div>

    <div class="credit"> &copy; copyright @
      <?php echo date('Y'); ?> All Rights Reserved <br> by <span>Pambi Egara Jeremiah & Stella Nyambura<br> </span>
      <span>Terms and Conditions Apply</span>
    </div>
  </section>

  <!-- footer section ends -->


  <script src="script.js"></script>
</body>

</html>