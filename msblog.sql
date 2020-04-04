-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 04, 2020 at 10:04 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `msblog`
--

-- --------------------------------------------------------

--
-- Table structure for table `journeys`
--

CREATE TABLE `journeys` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `author` text NOT NULL,
  `content` text NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `journeys`
--

INSERT INTO `journeys` (`id`, `title`, `author`, `content`, `created_date`) VALUES
(2, 'Deneme', 'mselek', '<p>Bu bir deneme yazısıdır</p>\r\n', '2020-04-02 17:12:05'),
(3, 'The First-Timer’s Travel Guide to Cappadocia, Turkey', 'mselek', '<p>When we first arrived in Cappadocia, it didn&rsquo;t feel like we were stepping out of a bus. It felt more like we were getting off a spaceship. It was the oddest-looking landscape I had ever seen with its mushroom-capped fairy chimneys and cities carved in stone. Cave dwelling has a long history in Cappadocia so people have likened its landscape to the Flintstones but to me, it felt more like the surface of the moon, completely alien and not of this earth.</p>\r\n\r\n<p>One of the things that surprised me the most about Turkey was its geographic diversity. Natural or man-made, there is so much to marvel at from its calcium travertines in Pamukkale to the minaret-filled skyline of Istanbul.&nbsp;But for me, Cappadocia topped them all. It&rsquo;s beauty, as you&rsquo;ll soon see, is out of this world.</p>\r\n\r\n<p>And if you think it looks stunning from the ground, wait till you see it from the skies.</p>\r\n', '2020-04-02 20:17:17'),
(4, 'Ankara', 'mselek', '<p>The heart of the Turkish Republic, Ankara, is the second largest city of Turkey after Istanbul. The city lies on the border where east between west. The European and Middle Eastern cultures merged and coloured the city&#39;s architecture, food, wine, nightlife, fashion and arts. Drop the anchor in Ankara, as its name suggests, cross the border between tradition and modernity.</p>\r\n', '2020-04-02 20:18:01');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`) VALUES
(1, 'Mahir Selek', 'mselek1297@gmail.com', 'mselek', '$5$rounds=535000$DpKOImR98lbsqigx$0FgmqM7fhCgYQswvmgyo.oTbLvV3Ixin02DvifHs5l9');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `journeys`
--
ALTER TABLE `journeys`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `journeys`
--
ALTER TABLE `journeys`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
