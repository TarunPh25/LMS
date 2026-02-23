const API_URL = "http://127.0.0.1:8001";

// State
let allStudents = [];
let currentFilter = 'all';

// DOM Elements
const studentListEl = document.getElementById('studentList');
const searchInput = document.getElementById('searchInput');
const modalBackdrop = document.getElementById('modalBackdrop');
const modalTitle = document.getElementById('modalTitle');
const studentForm = document.getElementById('studentForm');

// Stats Elements
const totalCountEl = document.getElementById('totalCount');
const activeCountEl = document.getElementById('activeCount');
const graduatedCountEl = document.getElementById('graduatedCount');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchStudents();
});

// ── API Functions ───────────────────────────────────────────────────────────

async function fetchStudents() {
    renderLoading();
    try {
        const response = await fetch(`${API_URL}/students/?limit=100`);
        if (!response.ok) throw new Error('Failed to fetch students');

        allStudents = await response.json();
        renderStudents();
        updateStats(); // Update stats based on the fetched data
    } catch (error) {
        showToast(error.message, 'danger');
        studentListEl.innerHTML = `<div class="p-4 text-center text-red-500">Error loading data</div>`;
    }
}

async function createStudent(data) {
    try {
        const response = await fetch(`${API_URL}/students/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to create student');
        }

        showToast('Student created successfully!');
        closeModal();
        fetchStudents();
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

async function updateStudent(id, data) {
    try {
        const response = await fetch(`${API_URL}/students/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to update student');
        }

        showToast('Student updated successfully!');
        closeModal();
        fetchStudents();
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

async function deleteStudent(id) {
    if (!confirm('Are you sure you want to delete this student?')) return;

    try {
        const response = await fetch(`${API_URL}/students/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete student');

        showToast('Student deleted successfully!');
        fetchStudents();
    } catch (error) {
        showToast(error.message, 'danger');
    }
}

// ── Rendering & Logic ───────────────────────────────────────────────────────

function renderLoading() {
    studentListEl.innerHTML = `
        <div class="loading-spinner">
            <i class="fa-solid fa-circle-notch fa-spin"></i>
        </div>
    `;
}

function renderStudents() {
    const searchTerm = searchInput.value.toLowerCase();

    const filtered = allStudents.filter(student => {
        // Filter by status tab
        if (currentFilter !== 'all' && student.status !== currentFilter) return false;

        // Filter by search
        const fullName = `${student.first_name} ${student.last_name}`.toLowerCase();
        const email = student.email.toLowerCase();
        return fullName.includes(searchTerm) || email.includes(searchTerm);
    });

    if (filtered.length === 0) {
        studentListEl.innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--text-muted);">No students found.</div>`;
        return;
    }

    studentListEl.innerHTML = filtered.map(student => `
        <div class="student-item">
            <div class="col-name">
                ${student.first_name} ${student.last_name}
            </div>
            <div class="col-contact">
                <span class="email">${student.email}</span>
                <span>${student.phone || '-'}</span>
            </div>
            <div class="col-date">
                ${new Date(student.enrollment_date).toLocaleDateString()}
            </div>
            <div class="col-status">
                <span class="status-badge status-${student.status}">
                    ${student.status}
                </span>
            </div>
            <div class="actions">
                <button class="action-btn edit" onclick="openModal('edit', ${student.id})">
                    <i class="fa-solid fa-pen"></i>
                </button>
                <button class="action-btn delete" onclick="deleteStudent(${student.id})">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function updateStats() {
    totalCountEl.textContent = allStudents.length;
    activeCountEl.textContent = allStudents.filter(s => s.status === 'active').length;
    graduatedCountEl.textContent = allStudents.filter(s => s.status === 'graduated').length;
}

function filterStudents(status) {
    currentFilter = status;

    // Update active visual state of tabs
    document.querySelectorAll('.nav-links li').forEach(li => {
        li.classList.remove('active');
        if (li.textContent.trim().toLowerCase().includes(status === 'all' ? 'all' : status)) {
            li.classList.add('active');
        }
    });

    renderStudents();
}

function handleSearch() {
    renderStudents();
}

// ── Modal Handling ──────────────────────────────────────────────────────────

function openModal(mode, studentId = null) {
    modalBackdrop.classList.remove('hidden');

    if (mode === 'create') {
        modalTitle.textContent = 'Add New Student';
        studentForm.reset();
        document.getElementById('studentId').value = '';
        // Set default date to today for UX
        // document.getElementById('dob').valueAsDate = new Date(); // Optional
    } else {
        modalTitle.textContent = 'Edit Student';
        const student = allStudents.find(s => s.id === studentId);
        if (student) {
            document.getElementById('studentId').value = student.id;
            document.getElementById('firstName').value = student.first_name;
            document.getElementById('lastName').value = student.last_name;
            document.getElementById('email').value = student.email;
            document.getElementById('phone').value = student.phone || '';
            document.getElementById('dob').value = student.date_of_birth || '';
            document.getElementById('status').value = student.status || 'active';
        }
    }
}

function closeModal() {
    modalBackdrop.classList.add('hidden');
}

// Close on backdrop click
modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) closeModal();
});

function handleFormSubmit(e) {
    e.preventDefault();

    const id = document.getElementById('studentId').value;
    const formData = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value || null,
        date_of_birth: document.getElementById('dob').value || null,
        status: document.getElementById('status').value
    };

    if (id) {
        updateStudent(id, formData);
    } else {
        createStudent(formData);
    }
}

// ── Utilities ───────────────────────────────────────────────────────────────

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const msgEl = toast.querySelector('.toast-message');

    msgEl.textContent = message;

    if (type === 'danger') {
        toast.classList.add('danger');
        toast.querySelector('.toast-icon').innerHTML = '<i class="fa-solid fa-exclamation-circle"></i>';
    } else {
        toast.classList.remove('danger');
        toast.querySelector('.toast-icon').innerHTML = '<i class="fa-solid fa-check-circle"></i>';
    }

    toast.classList.remove('hidden');

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}
