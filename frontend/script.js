const form = document.getElementById('resumeForm');
const resumeFile = document.getElementById('resumeFile');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const errorDiv = document.getElementById('error');

const skillsList = document.getElementById('skillsList');
const educationList = document.getElementById('educationList');
const experienceText = document.getElementById('experienceText');
const jobMatchesList = document.getElementById('jobMatchesList');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  results.classList.add('hidden');
  errorDiv.classList.add('hidden');
  loading.classList.remove('hidden');

  const file = resumeFile.files[0];
  if (!file) {
    alert("Please select a file!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze-resume", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Error analyzing resume");
    }

    const data = await response.json();

    // Display Skills
    skillsList.innerHTML = "";
    data.skills.forEach(skill => {
      const li = document.createElement("li");
      li.textContent = skill;
      skillsList.appendChild(li);
    });

    // Display Education
    educationList.innerHTML = "";
    data.education.forEach(edu => {
      const li = document.createElement("li");
      li.textContent = edu;
      educationList.appendChild(li);
    });

    // Display Experience
    experienceText.textContent = data.experience;

    // Display Job Matches
    jobMatchesList.innerHTML = "";
    if (data.job_matches.length > 0) {
      data.job_matches.forEach(job => {
        const li = document.createElement("li");
        li.textContent = `${job.job_title} (Match Score: ${job.match_score})`;
        jobMatchesList.appendChild(li);
      });
    } else {
      jobMatchesList.innerHTML = "<li>No matches found</li>";
    }

    loading.classList.add('hidden');
    results.classList.remove('hidden');

  } catch (err) {
    loading.classList.add('hidden');
    errorDiv.textContent = err.message;
    errorDiv.classList.remove('hidden');
  }
});
