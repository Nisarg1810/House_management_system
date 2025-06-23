document.addEventListener('DOMContentLoaded', () => {
    // Theme Switcher
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;

    // Check for saved theme preference
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
        if(darkModeToggle) darkModeToggle.checked = true;
    }

    if(darkModeToggle){
        darkModeToggle.addEventListener('change', () => {
            if (darkModeToggle.checked) {
                body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark');
            } else {
                body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // Modal Handling - Global function to open modals
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.style.display = 'block';
    }

    // Close modal functionality
    const closeBtns = document.querySelectorAll('.modal .close-btn');
    const modals = document.querySelectorAll('.modal');

    function closeModalElement(modalElement) {
        if (modalElement) modalElement.style.display = 'none';
    }

    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modals.forEach(modal => closeModalElement(modal));
        });
    });

    window.addEventListener('click', (event) => {
        modals.forEach(modal => {
            if (event.target === modal) {
                closeModalElement(modal);
            }
        });
    });
    
    // Form Submissions (Client-side placeholders)
    const addStockForm = document.getElementById('addStockForm');
    const stockListUl = document.getElementById('stockList') || document.getElementById('fullStockList'); // Check both dashboard and inventory page

    if (addStockForm && stockListUl) {
        addStockForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const itemName = document.getElementById('stockItemName').value;
            const itemQty = document.getElementById('stockItemQty').value;
            const itemUnit = document.getElementById('stockItemUnit').value || 'pcs';
            const itemExpiry = document.getElementById('stockItemExpiry').value;

            if (itemName && itemQty) {
                const listItem = document.createElement('li');
                listItem.innerHTML = `${itemName} - ${itemQty} ${itemUnit} ${itemExpiry ? `(Expires: ${itemExpiry})` : ''} <span class="text-danger expiry-soon-badge" style="display:none;">Expires Soon!</span>`;
                
                if (itemExpiry) {
                    const expiryDate = new Date(itemExpiry);
                    const today = new Date();
                    const sevenDaysFromNow = new Date(new Date().setDate(today.getDate() + 7)); // Ensure today is not modified
                    if (expiryDate <= sevenDaysFromNow && expiryDate >= new Date()) { 
                        const badge = listItem.querySelector('.expiry-soon-badge');
                        if(badge) badge.style.display = 'inline';
                    }
                }

                if (stockListUl.querySelector('li')?.textContent.includes('No items in stock') || stockListUl.querySelector('li')?.textContent.includes('Loading inventory...')) {
                    stockListUl.innerHTML = ''; 
                }
                stockListUl.appendChild(listItem);
                addStockForm.reset();
                closeModalElement(document.getElementById('addStockModal'));
                updateStockNeeds(); 
                updateSmartSuggestions(itemName, 'stock'); 
            }
        });
    }

    const addExpenseForm = document.getElementById('addExpenseForm');
    const expenseListUl = document.getElementById('expenseList') || document.getElementById('fullExpenseList'); // Check both dashboard and expenses page
    const totalExpensesTodaySpan = document.getElementById('totalExpensesToday');

    if (addExpenseForm && expenseListUl) {
        addExpenseForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const description = document.getElementById('expenseDescription').value;
            const amount = parseFloat(document.getElementById('expenseAmount').value);
            const category = document.getElementById('expenseCategory').value;
            const date = document.getElementById('expenseDate').value;

            if (description && amount && category && date) {
                const listItem = document.createElement('li');
                listItem.textContent = `${date} - ${description} ($${amount.toFixed(2)}) - Category: ${category}`;
                
                if (expenseListUl.querySelector('li')?.textContent.includes('No expenses logged yet') || expenseListUl.querySelector('li')?.textContent.includes('Loading expenses...')) {
                    expenseListUl.innerHTML = ''; 
                }
                expenseListUl.appendChild(listItem);

                if(totalExpensesTodaySpan){
                    const todayStr = new Date().toISOString().split('T')[0];
                    if (date === todayStr) {
                        let currentTotal = parseFloat(totalExpensesTodaySpan.textContent.replace('$', '')) || 0;
                        currentTotal += amount;
                        totalExpensesTodaySpan.textContent = `$${currentTotal.toFixed(2)}`;
                    }
                }
                
                addExpenseForm.reset();
                closeModalElement(document.getElementById('addExpenseModal'));
                updateBudgetOverview(); 
                updateSmartSuggestions(description, 'expense'); 
            }
        });
    }
    
    function renderBudgetChart() {
        const budgetChartPlaceholder = document.getElementById('budgetChartPlaceholder');
        if (budgetChartPlaceholder && typeof Chart !== 'undefined') {
            // Clear previous chart if exists
            let chartStatus = Chart.getChart("budgetChart"); 
            if (chartStatus != undefined) {
              chartStatus.destroy();
            }
            budgetChartPlaceholder.innerHTML = '<canvas id="budgetChart"></canvas>'; 
            const ctx = document.getElementById('budgetChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie', 
                data: {
                    labels: ['Income', 'Expenses', 'Savings'],
                    datasets: [{
                        label: 'Budget Overview',
                        data: [
                            parseFloat(document.getElementById('totalIncome')?.textContent.replace('$', '') || 0),
                            parseFloat(document.getElementById('monthlyExpenses')?.textContent.replace('$', '') || 0),
                            parseFloat(document.getElementById('savings')?.textContent.replace('$', '') || 0)
                        ],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.7)', 
                            'rgba(255, 99, 132, 0.7)',  
                            'rgba(54, 162, 235, 0.7)'   
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Budget Distribution'
                        }
                    }
                }
            });
        } else if (budgetChartPlaceholder) {
            budgetChartPlaceholder.innerHTML = '<p>Chart library (Chart.js) not loaded or placeholder not found.</p>';
        }
    }
    
    function updateBudgetOverview() {
        renderBudgetChart(); 
    }

    const lowStockListUl = document.getElementById('lowStockList');
    function updateStockNeeds() {
        if (!stockListUl || !lowStockListUl) return;

        const items = Array.from(stockListUl.querySelectorAll('li'));
        const lowStockItems = [];
        const threshold = 5; 

        items.forEach(item => {
            const text = item.textContent;
            if(text.includes('No items in stock') || text.includes('Loading inventory...')) return;
            const match = text.match(/- (\d+) (.+?) /); 
            if (match && parseInt(match[1]) <= threshold) {
                lowStockItems.push(text.split(' (Expires:')[0]); 
            }
        });

        lowStockListUl.innerHTML = ''; 
        if (lowStockItems.length > 0) {
            lowStockItems.forEach(itemName => {
                const li = document.createElement('li');
                li.textContent = `Low on: ${itemName}`;
                lowStockListUl.appendChild(li);
            });
        } else {
            lowStockListUl.innerHTML = '<li>All stocked up!</li>';
        }
    }
    
    const suggestionListUl = document.getElementById('suggestionList');
    const itemFrequency = {}; 

    function updateSmartSuggestions(itemName, type) { 
        if (!suggestionListUl) return;

        itemFrequency[itemName] = (itemFrequency[itemName] || 0) + 1;

        const sortedItems = Object.entries(itemFrequency)
            .sort(([,a],[,b]) => b-a)
            .slice(0, 3);

        suggestionListUl.innerHTML = '';
        if (sortedItems.length > 0) {
            sortedItems.forEach(([name, freq]) => {
                const li = document.createElement('li');
                li.textContent = `Consider: ${name} (used ${freq} times)`;
                suggestionListUl.appendChild(li);
            });
        } else {
            suggestionListUl.innerHTML = '<li>No suggestions right now.</li>';
        }
    }

    const voiceStatusDiv = document.getElementById('voiceStatus');
    const stopListeningBtn = document.getElementById('stopListeningBtn');
    const voiceInputTrigger = document.createElement('button');
    voiceInputTrigger.innerHTML = '<i class="fas fa-microphone"></i> Voice';
    voiceInputTrigger.classList.add('add-item-btn'); 
    voiceInputTrigger.style.marginLeft = '10px';
    voiceInputTrigger.addEventListener('click', () => {
        openModal('voiceInputModal');
        startVoiceRecognition(); 
    });
    
    const stockCardHeader = document.querySelector('#stock-inventory-card .card-header');
    if (stockCardHeader) {
        stockCardHeader.appendChild(voiceInputTrigger);
    } else {
        // Attempt to add to inventory page if dashboard card not found
        const inventoryPageHeader = document.querySelector('.page-header h2 i.fa-boxes')?.closest('.page-header');
        if(inventoryPageHeader && inventoryPageHeader.querySelector('button.add-item-btn')){
            inventoryPageHeader.querySelector('button.add-item-btn').insertAdjacentElement('afterend', voiceInputTrigger);
        }
    }


    function startVoiceRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            if(voiceStatusDiv) voiceStatusDiv.textContent = 'Voice recognition not supported.';
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        if(voiceStatusDiv) voiceStatusDiv.textContent = 'Listening...';

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript.trim().toLowerCase();
            if(voiceStatusDiv) voiceStatusDiv.textContent = `Heard: "${transcript}" - Processing...`;
            processVoiceCommand(transcript);
        };

        recognition.onerror = (event) => {
            if(voiceStatusDiv) voiceStatusDiv.textContent = `Error: ${event.error}`;
        };

        recognition.onend = () => {
            if(voiceStatusDiv && voiceStatusDiv.textContent === 'Listening...') { 
                 voiceStatusDiv.textContent = 'Stopped. Try again?';
            }
        };
        
        recognition.start();

        if(stopListeningBtn) {
            stopListeningBtn.onclick = () => {
                recognition.stop();
                if(voiceStatusDiv) voiceStatusDiv.textContent = 'Stopped by user.';
                closeModalElement(document.getElementById('voiceInputModal'));
            };
        }
    }

    function processVoiceCommand(command) {
        const stockRegex = /add (\d+) (.+?) to stock/i;
        const expenseRegex = /add (\d+(?:\.\d+)?) for (.+?) as expense/i;

        let match = command.match(stockRegex);
        if (match) {
            const qty = match[1];
            const name = match[2];
            if(document.getElementById('stockItemName')) document.getElementById('stockItemName').value = name;
            if(document.getElementById('stockItemQty')) document.getElementById('stockItemQty').value = qty;
            if(addStockForm) addStockForm.requestSubmit ? addStockForm.requestSubmit() : addStockForm.submit();
            if(voiceStatusDiv) voiceStatusDiv.textContent = `Added ${qty} ${name} to stock.`;
            setTimeout(() => closeModalElement(document.getElementById('voiceInputModal')), 1500);
            return;
        }

        match = command.match(expenseRegex);
        if (match) {
            const amount = match[1];
            const description = match[2];
            if(document.getElementById('expenseDescription')) document.getElementById('expenseDescription').value = description;
            if(document.getElementById('expenseAmount')) document.getElementById('expenseAmount').value = amount;
            if(document.getElementById('expenseCategory')) document.getElementById('expenseCategory').value = 'other'; // Default
            if(document.getElementById('expenseDate')) document.getElementById('expenseDate').valueAsDate = new Date();
            if(addExpenseForm) addExpenseForm.requestSubmit ? addExpenseForm.requestSubmit() : addExpenseForm.submit();
            if(voiceStatusDiv) voiceStatusDiv.textContent = `Added expense: $${amount} for ${description}.`;
            setTimeout(() => closeModalElement(document.getElementById('voiceInputModal')), 1500);
            return;
        }

        if(voiceStatusDiv) voiceStatusDiv.textContent = `Unknown command: "${command}"`;
    }

    const calendarPlaceholder = document.getElementById('calendarPlaceholder');
    if (calendarPlaceholder) {
        const events = [
            { date: '2025-07-01', title: 'Pay Electricity Bill' },
            { date: '2025-07-05', title: 'Grocery Shopping Day' },
            { date: '2025-07-15', title: 'House Maintenance Check' }
        ];
        let upcomingEventsHTML = '<h4>Upcoming:</h4><ul>';
        const today = new Date().toISOString().split('T')[0];
        const futureEvents = events.filter(event => event.date >= today).slice(0,3);
        if (futureEvents.length > 0) {
            futureEvents.forEach(event => {
                upcomingEventsHTML += `<li>${new Date(event.date).toLocaleDateString()}: ${event.title}</li>`;
            });
            upcomingEventsHTML += '</ul>';
        } else {
            upcomingEventsHTML = '<p>No upcoming events scheduled.</p>';
        }
        calendarPlaceholder.innerHTML = upcomingEventsHTML;
    }
    
    const stockSearchInput = document.getElementById('stockSearch') || document.getElementById('inventorySearch');
    const stockSortSelect = document.getElementById('stockSort') || document.getElementById('inventorySort');

    function filterAndSortStock() {
        if (!stockListUl) return;
        const searchTerm = stockSearchInput ? stockSearchInput.value.toLowerCase() : '';
        const sortBy = stockSortSelect ? stockSortSelect.value : 'name_asc';
        
        let items = Array.from(stockListUl.querySelectorAll('li'));
        if(items.length === 1 && (items[0].textContent.includes('No items in stock') || items[0].textContent.includes('Loading inventory...'))) return;


        items.forEach(item => {
            const itemName = item.textContent.toLowerCase();
            if (itemName.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
        
        items = items.filter(item => item.style.display !== 'none');

        items.sort((a, b) => {
            const textA = a.textContent;
            const textB = b.textContent;
            
            const nameA = textA.split(' - ')[0];
            const nameB = textB.split(' - ')[0];
            
            const qtyA = parseInt(textA.match(/- (\d+) /)?.[1] || 0);
            const qtyB = parseInt(textB.match(/- (\d+) /)?.[1] || 0);
            
            const expiryA = new Date(textA.match(/Expires: (.*?)\)/)?.[1] || '9999-12-31');
            const expiryB = new Date(textB.match(/Expires: (.*?)\)/)?.[1] || '9999-12-31');

            switch (sortBy) {
                case 'name_asc': return nameA.localeCompare(nameB);
                case 'name_desc': return nameB.localeCompare(nameA);
                case 'qty_low': return qtyA - qtyB;
                case 'qty_high': return qtyB - qtyA;
                case 'expiry_soon': return expiryA - expiryB;
                default: return 0;
            }
        });

        items.forEach(item => stockListUl.appendChild(item));
    }

    if (stockSearchInput) stockSearchInput.addEventListener('input', filterAndSortStock);
    if (stockSortSelect) stockSortSelect.addEventListener('change', filterAndSortStock);

    // Initial calls
    if(document.getElementById('budgetChartPlaceholder')) updateBudgetOverview();
    if(document.getElementById('stockList') || document.getElementById('fullStockList')) updateStockNeeds();
    
    console.log('Smart House Manager script loaded and initialized.');
});