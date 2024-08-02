document.addEventListener("DOMContentLoaded", function() {
    // Get all paragraphs within the description class
    var descriptionParagraphs = document.querySelectorAll('.description p');

    descriptionParagraphs.forEach(paragraph => {
        var textLength = paragraph.textContent.length;

        // Define minimum and maximum font sizes
        var minFontSize = 17; // Minimum font size in pixels
        var maxFontSize = 32; // Maximum font size in pixels

        // Calculate font size based on the length of the text
        var newFontSize = Math.max(minFontSize, maxFontSize - (textLength / 20)); // Adjust the divisor as needed

        // Apply the calculated font size
        paragraph.style.fontSize = newFontSize + 'px';
    });

    // Initialize dropdowns and apply filters
    updateDropdowns();
});
document.addEventListener('DOMContentLoaded', () => {
    const speakerFilter = document.getElementById('speaker-filter');
    const categoryFilter = document.getElementById('category-filter');
    const tagFilter = document.getElementById('tag-filter');
    const resetButton = document.getElementById('reset-filters');

    // Get all video items
    const videoItems = Array.from(document.querySelectorAll('.video-item'));

    // Function to extract and return categories and tags from video items
    function extractCategoriesAndTags() {
        const categories = new Set();
        const tags = new Set();

        videoItems.forEach(item => {
            const cat1 = item.getAttribute('data-cat1');
            const cat2 = item.getAttribute('data-cat2');
            const itemTags = item.getAttribute('data-tags').split(',').map(tag => tag.trim());

            // Add cat1 to categories if it has a value and is not "None"
            if (cat1 && cat1.trim().toLowerCase() !== 'none') {
                categories.add(cat1);
            }

            // Add cat2 to categories if it is not empty, null, or "None"
            if (cat2 && cat2.trim() !== '' && cat2.trim().toLowerCase() !== 'none') {
                categories.add(cat2);
            }

            // Add tags to tags set
            itemTags.forEach(tag => tags.add(tag));
        });

        return { categories, tags };
    }

    // Function to update dropdowns based on selected values
    function updateDropdowns() {
        const selectedSpeaker = speakerFilter.value;
        const selectedCategory = categoryFilter.value;

        const { categories, tags } = extractCategoriesAndTags();

        const filteredCategories = new Set();
        const filteredTags = new Set();

        videoItems.forEach(item => {
            const speakerId = item.getAttribute('data-speaker');
            const cat1 = item.getAttribute('data-cat1');
            const cat2 = item.getAttribute('data-cat2');
            const itemTags = item.getAttribute('data-tags').split(',').map(tag => tag.trim());

            if ((!selectedSpeaker || speakerId === selectedSpeaker) &&
                (!selectedCategory || cat1 === selectedCategory || cat2 === selectedCategory)) {
                itemTags.forEach(tag => filteredTags.add(tag));
                if (cat1 && cat1.trim().toLowerCase() !== 'none') filteredCategories.add(cat1);
                if (cat2 && cat2.trim().toLowerCase() !== 'none') filteredCategories.add(cat2);
            }
        });

        // Sort categories and tags case-insensitively
        const sortedCategories = Array.from(filteredCategories).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));
        const sortedTags = Array.from(filteredTags).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));

        // Update category dropdown
        categoryFilter.innerHTML = '<option value="">Tous les thèmes</option>';
        sortedCategories.forEach(cat => {
            categoryFilter.innerHTML += `<option value="${cat}" ${cat === selectedCategory ? 'selected' : ''}>${cat}</option>`;
        });

        // Update tag dropdown
        tagFilter.innerHTML = '<option value="">Tous les tags</option>';
        sortedTags.forEach(tag => {
            tagFilter.innerHTML += `<option value="${tag}">${tag}</option>`;
        });

        // Apply filters to video items
        filterVideos();
    }

    // Function to filter video items based on selected values
    function filterVideos() {
        const selectedSpeaker = speakerFilter.value;
        const selectedCategory = categoryFilter.value;
        const selectedTag = tagFilter.value;

        videoItems.forEach(item => {
            const speakerId = item.getAttribute('data-speaker');
            const tags = item.getAttribute('data-tags').split(',').map(tag => tag.trim());
            const cat1 = item.getAttribute('data-cat1');
            const cat2 = item.getAttribute('data-cat2');

            let showItem = true;

            if (selectedSpeaker && speakerId !== selectedSpeaker) {
                showItem = false;
            }

            if (selectedCategory && (cat1 !== selectedCategory && cat2 !== selectedCategory)) {
                showItem = false;
            }

            if (selectedTag && !tags.includes(selectedTag)) {
                showItem = false;
            }

            item.style.display = showItem ? 'block' : 'none';
        });
    }

    // Function to reset all filters and dropdowns
    function resetFilters() {
        speakerFilter.value = '';
        categoryFilter.value = '';
        tagFilter.value = '';
        updateDropdowns();
        filterVideos();
    }

    // Event listeners for dropdowns and reset button
    speakerFilter.addEventListener('change', () => {
        updateDropdowns();
        filterVideos();
    });

    categoryFilter.addEventListener('change', () => {
        updateDropdowns();
        filterVideos();
    });

    tagFilter.addEventListener('change', filterVideos);

    resetButton.addEventListener('click', resetFilters);

    // Initial setup
    updateDropdowns();
    filterVideos();
});
