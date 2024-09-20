var acAnimated = {Plugins: {}};
/* SplitText Plugin - Starts */
acAnimated.Plugins.SplitText = function(element, options) {
	if (!options.hasOwnProperty("words")) options.words = 1;
	if (!options.hasOwnProperty("chars")) options.chars = 1;
	if (!options.hasOwnProperty("spacing")) options.spacing = 5;
	this.searchTextNodes = function(element) {
		var foundTextNodes = [];
		if (element == null || element == undefined) return foundTextNodes;
		for (var i=0; i<=element.childNodes.length-1; i++) {
			var node = element.childNodes[i];
			if (node.nodeName == "#text") { //text found
				foundTextNodes.push(node);
			} else {
				var foundTextNodes = foundTextNodes.concat(this.searchTextNodes(node));
			}
		}
		return foundTextNodes;
	}
	this.createElement = function(text, relatedNode) {
		var node = document.createElement("div");
		var nodeText = document.createTextNode(text);
		node.nodeText = nodeText;
		node.appendChild(nodeText);
		node.style.display = "inline-block";
		node.style.position = "relative";
		if (text.trim() == "") node.style.width = String(options.spacing) + "px";
		relatedNode.parentNode.insertBefore(node, relatedNode);
		return node;
	}
	this.splitCharacters = function(textNode) {
		var characters = textNode.nodeValue.toString();
		var chars = [];
		if (characters.trim() != "") {
			for (var c=0; c<=characters.length-1; c++) {
				var character = characters.substr(c, 1)
				var char = this.createElement(character, textNode);
				if (character.trim() != "") chars.push(char);
			}
			textNode.parentNode.removeChild(textNode);
		}
		return chars;
	}
	this.splitWords = function(textNode) {
		var textWords = textNode.nodeValue.toString().split(" ");
		var words = [];
		for (var w=0; w<=textWords.length-1; w++) {
			var textWord = textWords[w];
			var word = this.createElement(textWord, textNode);
			if (textWord.trim() != "") words.push(word);
			if (w < textWords.length-1) this.createElement(" ", textNode); //spacing for word
		}
		textNode.parentNode.removeChild(textNode);
		return words;
	}
	this.splitTextNodes = function(textNodes) {
		var splitText = {words: [], chars: []};
		for (var i=0; i<=textNodes.length-1; i++) {
			var textNode = textNodes[i];
			if (options.words == 0) {
				splitText.chars = splitText.chars.concat(this.splitCharacters(textNode));
			} else {
				var words = this.splitWords(textNode);
				if (options.chars == 1) {
					for (var w=0; w<=words.length-1; w++) {
						word = words[w];
						var chars = this.splitCharacters(word.nodeText);
						splitText.chars = splitText.chars.concat(chars);
						word.chars = chars;
					}
				}
				splitText.words = splitText.words.concat(words);
			}
		}
		return splitText;
	}
	var textNodes = this.searchTextNodes(element);
	var splitText = this.splitTextNodes(textNodes);
	return splitText;
}

var text = document.body.querySelector("#quote");
var splitText = acAnimated.Plugins.SplitText(text, {words: 1, chars: 1, spacing: 10});
console.log('splitText',splitText)
// Type one
// new TimelineMax({repeat:2220}).staggerFrom(splitText.chars, 0.8, { y: 100, opacity: 0 }, 0.05);

// // Type Two
// new TimelineMax({repeat:2220}).staggerFrom(splitText.chars, 0.75, { ease:Back.easeOuteaseOut,top:"+=750", y: 20 }, 0.08)
// .to(splitText.chars, 2, {y:0, ease:Elastic.easeInOut}, "+=1");

//  Type Three
 new TimelineMax({repeat:2220}).staggerFrom(splitText.chars, 0.75, { autoAlpha:0 }, 0.08)
.to(splitText.chars, 2, {autoAlpha:1});



//scramble text
const textElements = document.querySelectorAll('h2.h1.vision');
const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
const interval = 200;  // Slower interval (in milliseconds)

function scrambleText(element) {
    const originalText = element.textContent;
    let counter = 0;

    function scramble() {
        const scrambled = originalText.split('').map((char, i) => {
            if (i <= counter) return originalText[i];
            return characters[Math.floor(Math.random() * characters.length)];
        }).join('');

        element.textContent = scrambled;

        if (counter < originalText.length) {
            counter++;
            setTimeout(scramble, interval);
        }
    }

    scramble();
}

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = 1;  // Make the text visible
            scrambleText(entry.target);  // Trigger the scramble animation
            observer.unobserve(entry.target);  // Stop observing after animation
        }
    });
});

textElements.forEach(element => observer.observe(element));


// Project Section Animation
document.addEventListener('DOMContentLoaded', () => {
	const cards = document.querySelectorAll('.card');
  
	const cardObserver = new IntersectionObserver((entries, observer) => {
		entries.forEach(entry => {
			if (entry.isIntersecting) {
				entry.target.classList.add('in-view');
				observer.unobserve(entry.target); // Stop observing once in view
			}
		});
	}, {
		threshold: 0.1  // Trigger animation when 10% of the card is visible
	});
  
	cards.forEach(card => cardObserver.observe(card));
  });
  


  // Timeline Section Animation
  document.addEventListener('DOMContentLoaded', () => {
	const timelineItems = document.querySelectorAll('.timeline-item');
  
	const timelineObserver = new IntersectionObserver((entries, observer) => {
	  entries.forEach(entry => {
		if (entry.isIntersecting) {
		  entry.target.classList.add('in-view');
		  observer.unobserve(entry.target); // Stop observing once in view
		}
	  });
	}, {
	  threshold: 0.1 // Trigger animation when 10% of the timeline item is visible
	});
  
	timelineItems.forEach(item => timelineObserver.observe(item));
  });

  

  // JavaScript to add 'visible' class on scroll

document.addEventListener('DOMContentLoaded', function () {
	const toolsSection = document.querySelector('.section-lg');
	
	// Create an intersection observer
	const sectionObserver = new IntersectionObserver(entries => {
	  entries.forEach(entry => {
		if (entry.isIntersecting) {
		  toolsSection.classList.add('visible');
		}
	  });
	}, { threshold: 0.1 });
	
	// Observe the section
	sectionObserver.observe(toolsSection);
  });
  
 
  
  