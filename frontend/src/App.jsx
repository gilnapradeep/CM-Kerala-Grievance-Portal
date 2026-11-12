
import { useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  Navigate,
  useNavigate,
} from "react-router-dom";
import {
  LogOut,
  ShieldCheck,
  ClipboardList,
  RefreshCw,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

import api from "./services/api";
import Contact from "./pages/Contact";
import "./index.css";

/* -------------------- AUTHENTICATION HELPERS -------------------- */

function getRole() {
  return localStorage.getItem("role");
}

function Protected({ children, roles }) {
  const token = localStorage.getItem("access_token");

  if (!token) return <Navigate to="/login" replace />;

  if (roles && !roles.includes(getRole())) {
    return <Navigate to="/" replace />;
  }

  return children;
}

/* -------------------- NAVBAR -------------------- */

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");
  const role = getRole();

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("role");
    localStorage.removeItem("username");

    navigate("/login");
  }

  return (
    <nav className="navbar">
      <Link to="/" className="brand">
        <span className="brand-icon">CM</span>
        <span>
          Kerala <b>Grievance Portal</b>
        </span>
      </Link>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/about">About Us</Link>
        <Link to="/how-it-works">How It Works</Link>
        <Link to="/departments">Departments</Link>
        <Link to="/track">Track Grievance</Link>
        <Link to="/faq">FAQ</Link>
        <Link to="/contact">Contact Us</Link>

        {token && role === "CITIZEN" && (
          <Link to="/citizen">My Dashboard</Link>
        )}

        {token && role === "CMO_ADMIN" && (
          <Link to="/cmo">CMO Dashboard</Link>
        )}

        {token && role === "OFFICER" && (
          <Link to="/officer">Officer Dashboard</Link>
        )}

        {token ? (
          <button className="nav-button" onClick={logout}>
            <LogOut size={16} /> Logout
          </button>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link className="nav-cta" to="/register">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

/* -------------------- PUBLIC PAGES -------------------- */

function Home() {
  return (
    <>
      <section className="hero">
        <div className="hero-content">
          <span className="eyebrow">CITIZEN SERVICES • KERALA</span>

          <h1>
            Your voice matters.
            <br />
            <span>We are listening.</span>
          </h1>

          <p>
            Submit public grievances, track their progress and stay informed
            about the action taken by the concerned departments.
          </p>

          <div className="hero-actions">
            <Link className="primary-btn" to="/register">
              Submit a Grievance
            </Link>

            <Link className="outline-btn" to="/track">
              Track a Grievance
            </Link>
          </div>
        </div>

        <div className="hero-art">
          <div className="art-circle">
            <ShieldCheck size={90} />
          </div>

          <h3>Transparent. Accountable. Responsive.</h3>
          <p>A digital channel for citizen participation.</p>
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <span className="eyebrow">HOW IT WORKS</span>
          <h2>Grievance redressal made simple</h2>
          <p>Four simple steps to raise and follow up on your concern.</p>
        </div>

        <div className="steps-grid">
          {[
            ["01", "Register", "Create your citizen account securely."],
            ["02", "Submit", "Describe your issue and attach supporting files."],
            ["03", "Track", "Use your unique reference number to follow progress."],
            ["04", "Resolution", "Receive updates and share feedback after resolution."],
          ].map(([number, title, description]) => (
            <div className="step-card" key={number}>
              <span className="step-number">{number}</span>
              <h3>{title}</h3>
              <p>{description}</p>
            </div>
          ))}
        </div>
      </section>

      <footer>
        CM Kerala Grievance Portal · Recruitment prototype · Not an official
        Government of Kerala website.
      </footer>
    </>
  );
}

function About() {
  return (
    <main className="page-wrap">
      <div className="section-heading">
        <span className="eyebrow">ABOUT THE PORTAL</span>
        <h2>A digital channel for public grievance redressal</h2>
        <p>
          This portal demonstrates how citizens can submit grievances, follow
          their status and receive updates from the responsible departments.
        </p>
      </div>

      <div className="panel">
        <h3>Our objective</h3>
        <p>
          To provide a simple and transparent digital process for recording
          public concerns, routing them to the appropriate department and
          monitoring their progress.
        </p>

        <h3>Transparency and accountability</h3>
        <p>
          Citizens can use a unique reference number to track the progress of
          their grievances. Authorized administrators and officers can review
          submissions and record actions taken.
        </p>

        <h3>AI-assisted review</h3>
        <p>
          The prototype includes an AI assistant that can suggest a grievance
          category, department, priority and summary. These are preliminary
          recommendations and require human review.
        </p>
      </div>
    </main>
  );
}

function HowItWorks() {
  const steps = [
    ["1. Create an account", "Register using your name, email address, mobile number and password."],
    ["2. Submit your grievance", "Select the district and category, describe the issue and optionally attach supporting files."],
    ["3. Receive a reference number", "A unique reference number is generated after successful submission."],
    ["4. Department review", "The grievance can be reviewed and assigned to the concerned department or officer."],
    ["5. Track progress", "Check the grievance status and public status history using your reference number."],
    ["6. Share feedback", "After resolution, submit a rating and optional comments about the resolution."],
  ];

  return (
    <main className="page-wrap">
      <div className="section-heading">
        <span className="eyebrow">PROCESS</span>
        <h2>How the portal works</h2>
        <p>Follow these steps to submit and monitor a grievance.</p>
      </div>

      <div className="steps-grid">
        {steps.map(([title, description]) => (
          <div className="step-card" key={title}>
            <h3>{title}</h3>
            <p>{description}</p>
          </div>
        ))}
      </div>
    </main>
  );
}

function Departments() {
  const departments = [
    "General Administration",
    "Water Resources",
    "Public Works",
    "Health and Family Welfare",
    "Education",
    "Local Self Government",
    "Transport",
    "Electricity",
    "Sanitation",
  ];

  return (
    <main className="page-wrap">
      <div className="section-heading">
        <span className="eyebrow">DEPARTMENTS</span>
        <h2>Concerned departments</h2>
        <p>
          Grievances can be reviewed and routed to the relevant department.
          The department list shown here is illustrative for this prototype.
        </p>
      </div>

      <div className="steps-grid">
        {departments.map((department) => (
          <div className="step-card" key={department}>
            <h3>{department}</h3>
            <p>Responsible for reviewing relevant public grievances.</p>
          </div>
        ))}
      </div>
    </main>
  );
}

function FAQ() {
  const questions = [
    [
      "How do I submit a grievance?",
      "Register or log in to your citizen account, open the Submit Grievance page, complete the form and submit it.",
    ],
    [
      "How can I track my grievance?",
      "Use the Track Grievance page and enter the reference number generated when you submitted the grievance.",
    ],
    [
      "Can I attach supporting documents?",
      "Yes. The submission form accepts optional JPG, JPEG, PNG, PDF, DOC and DOCX attachments, subject to the configured file-size limit.",
    ],
    [
      "What do the grievance statuses mean?",
      "Submitted means the grievance has been received. Under Review means it is being examined. In Progress means action is being taken. Resolved means a resolution has been recorded. Reopened means it has been reopened for further attention.",
    ],
    [
      "Can I give feedback?",
      "A citizen can submit a rating and optional comments after the grievance is marked as resolved.",
    ],
    [
      "Are AI recommendations final decisions?",
      "No. AI output is only a preliminary recommendation. An authorized human reviewer must review it.",
    ],
  ];

  return (
    <main className="page-wrap">
      <div className="section-heading">
        <span className="eyebrow">HELP CENTRE</span>
        <h2>Frequently asked questions</h2>
        <p>Answers to common questions about using the portal.</p>
      </div>

      <div className="panel">
        {questions.map(([question, answer]) => (
          <div className="history-item" key={question}>
            <h3>{question}</h3>
            <p>{answer}</p>
          </div>
        ))}
      </div>
    </main>
  );
}

/* -------------------- LOGIN AND REGISTRATION -------------------- */

function AuthPage({ register = false }) {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
    first_name: "",
    last_name: "",
    email: "",
    mobile: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function change(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function submit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (register) {
        await api.post("/accounts/register/", form);

        alert("Registration successful. Please log in.");
        navigate("/login");
      } else {
        const response = await api.post("/accounts/login/", {
          username: form.username,
          password: form.password,
        });

        localStorage.setItem("access_token", response.data.access);
        localStorage.setItem("refresh_token", response.data.refresh);

        const profile = await api.get("/accounts/profile/");

        localStorage.setItem("role", profile.data.role);
        localStorage.setItem("username", profile.data.username);

        const role = profile.data.role;

        navigate(
          role === "CMO_ADMIN"
            ? "/cmo"
            : role === "OFFICER"
              ? "/officer"
              : "/citizen"
        );
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          JSON.stringify(
            err.response?.data || "Request failed. Check your backend."
          )
      );

      // Avoid leaving an invalid or incomplete login session.
      if (!register) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("role");
        localStorage.removeItem("username");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-wrap">
      <form className="form-card" onSubmit={submit}>
        <span className="eyebrow">
          {register ? "CITIZEN ACCOUNT" : "WELCOME BACK"}
        </span>

        <h2>{register ? "Create your account" : "Sign in to continue"}</h2>

        <p className="muted">
          {register
            ? "Register to submit and track grievances."
            : "Access your grievance portal dashboard."}
        </p>

        {register && (
          <>
            <div className="two-col">
              <Field
                label="First name"
                name="first_name"
                value={form.first_name}
                onChange={change}
                required
              />

              <Field
                label="Last name"
                name="last_name"
                value={form.last_name}
                onChange={change}
                required
              />
            </div>

            <Field
              label="Email address"
              name="email"
              type="email"
              value={form.email}
              onChange={change}
              required
            />

            <Field
              label="Mobile number"
              name="mobile"
              value={form.mobile}
              onChange={change}
              required
            />
          </>
        )}

        <Field
          label="Username"
          name="username"
          value={form.username}
          onChange={change}
          required
        />

        <Field
          label="Password"
          name="password"
          type="password"
          value={form.password}
          onChange={change}
          required
        />

        {error && <div className="error-message">{error}</div>}

        <button className="primary-btn full-btn" disabled={loading}>
          {loading
            ? "Please wait..."
            : register
              ? "Create Account"
              : "Login"}
        </button>

        <p className="form-bottom">
          {register ? "Already registered? " : "New citizen? "}
          <Link to={register ? "/login" : "/register"}>
            {register ? "Login" : "Create an account"}
          </Link>
        </p>
      </form>
    </div>
  );
}

function Field({ label, ...props }) {
  return (
    <label className="field">
      <span>{label}</span>
      <input {...props} />
    </label>
  );
}

/* -------------------- CITIZEN DASHBOARD -------------------- */

function CitizenDashboard() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function load() {
    setLoading(true);

    try {
      const response = await api.get("/grievances/");

      setItems(
        Array.isArray(response.data)
          ? response.data
          : response.data.results || []
      );

      setError("");
    } catch {
      setError("Unable to load grievances. Please log in again.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submitFeedback(item) {
    const ratingInput = window.prompt(
      "Rate the resolution from 1 to 5:"
    );

    if (ratingInput === null) return;

    const rating = Number(ratingInput);

    if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
      alert("Please enter a rating between 1 and 5.");
      return;
    }

    const comments =
      window.prompt("Share your feedback (optional):") || "";

    try {
      await api.post(
        `/grievances/${encodeURIComponent(item.reference_number)}/feedback/`,
        { rating, comments }
      );

      alert("Feedback submitted successfully.");
      load();
    } catch (err) {
      alert(
        JSON.stringify(
          err.response?.data || "Feedback submission failed."
        )
      );
    }
  }

  const resolved = items.filter(
    (item) => item.status === "RESOLVED"
  ).length;

  const pending = items.length - resolved;

  return (
    <DashboardLayout
      title="Citizen Dashboard"
      subtitle="View and manage your submitted grievances."
    >
      <div className="stats-grid">
        <Stat
          title="Total grievances"
          value={items.length}
          icon={<ClipboardList />}
        />

        <Stat
          title="Pending"
          value={pending}
          icon={<RefreshCw />}
        />

        <Stat
          title="Resolved"
          value={resolved}
          icon={<CheckCircle />}
        />
      </div>

      <div className="panel">
        <div className="panel-heading">
          <h3>My Grievances</h3>

          <div>
            <button
              className="outline-btn small-btn"
              onClick={load}
              disabled={loading}
            >
              {loading ? "Loading..." : "Refresh"}
            </button>

            <Link className="primary-btn small-btn" to="/submit">
              + New Grievance
            </Link>
          </div>
        </div>

        {error && <p className="error-message">{error}</p>}

        <GrievanceTable items={items} />

        {items.some((item) => item.status === "RESOLVED") && (
          <div className="feedback-section">
            <h3>Resolution feedback</h3>
            <p className="muted">
              You can share feedback about grievances marked as resolved.
            </p>

            {items
              .filter((item) => item.status === "RESOLVED")
              .map((item) => (
                <div className="officer-actions" key={item.id}>
                  <div>
                    <b>{item.reference_number}</b>
                    <small>{item.subject}</small>
                  </div>

                  <button
                    className="primary-btn tiny-btn"
                    onClick={() => submitFeedback(item)}
                  >
                    Give Feedback
                  </button>
                </div>
              ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

/* -------------------- SUBMIT GRIEVANCE -------------------- */

function SubmitGrievance() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    district: "KANNUR",
    category: "OTHER",
    subject: "",
    description: "",
  });

  const [files, setFiles] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      const data = new FormData();

      Object.entries(form).forEach(([key, value]) => {
        data.append(key, value);
      });

      files.forEach((file) => {
        data.append("uploaded_files", file);
      });

      const response = await api.post("/grievances/", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      alert(
        `Grievance submitted! Reference: ${response.data.reference_number}`
      );

      navigate("/citizen");
    } catch (err) {
      setError(
        JSON.stringify(
          err.response?.data || "Submission failed."
        )
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <DashboardLayout
      title="Submit a Grievance"
      subtitle="Provide accurate details so your concern can be reviewed."
    >
      <form className="panel form-panel" onSubmit={submit}>
        <div className="two-col">
          <label className="field">
            <span>District</span>

            <select
              value={form.district}
              onChange={(e) =>
                setForm({ ...form, district: e.target.value })
              }
            >
              {[
                "THIRUVANANTHAPURAM",
                "KOLLAM",
                "PATHANAMTHITTA",
                "ALAPPUZHA",
                "KOTTAYAM",
                "IDUKKI",
                "ERNAKULAM",
                "THRISSUR",
                "PALAKKAD",
                "MALAPPURAM",
                "KOZHIKODE",
                "WAYANAD",
                "KANNUR",
                "KASARAGOD",
              ].map((district) => (
                <option key={district}>{district}</option>
              ))}
            </select>
          </label>

          <label className="field">
            <span>Category</span>

            <select
              value={form.category}
              onChange={(e) =>
                setForm({ ...form, category: e.target.value })
              }
            >
              {[
                "INFRASTRUCTURE",
                "HEALTHCARE",
                "EDUCATION",
                "PUBLIC_SERVICES",
                "WATER",
                "ELECTRICITY",
                "TRANSPORT",
                "SANITATION",
                "OTHER",
              ].map((category) => (
                <option key={category}>{category}</option>
              ))}
            </select>
          </label>
        </div>

        <Field
          label="Subject"
          value={form.subject}
          onChange={(e) =>
            setForm({ ...form, subject: e.target.value })
          }
          required
        />

        <label className="field">
          <span>Description</span>

          <textarea
            rows="6"
            value={form.description}
            onChange={(e) =>
              setForm({ ...form, description: e.target.value })
            }
            required
          />
        </label>

        <label className="field">
          <span>Attachments (optional, max 5 MB each)</span>

          <input
            type="file"
            multiple
            accept=".jpg,.jpeg,.png,.pdf,.doc,.docx"
            onChange={(e) =>
              setFiles(Array.from(e.target.files || []))
            }
          />
        </label>

        {files.length > 0 && (
          <p className="muted">
            {files.length} file(s) selected.
          </p>
        )}

        {error && <div className="error-message">{error}</div>}

        <button className="primary-btn" disabled={loading}>
          {loading ? "Submitting..." : "Submit Grievance"}
        </button>
      </form>
    </DashboardLayout>
  );
}

/* -------------------- TRACK GRIEVANCE -------------------- */

function TrackGrievance() {
  const [reference, setReference] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function track(e) {
    e.preventDefault();

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await api.get(
        `/grievances/track/${encodeURIComponent(reference.trim())}/`
      );

      setResult(response.data);
    } catch {
      setError("Grievance not found. Check your reference number.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-wrap">
      <div className="section-heading">
        <span className="eyebrow">STATUS CHECK</span>
        <h2>Track your grievance</h2>
        <p>
          Enter the reference number received after submission.
        </p>
      </div>

      <form className="track-form" onSubmit={track}>
        <input
          placeholder="Example: CMK-20261112-XXXXXXXX"
          value={reference}
          onChange={(e) => setReference(e.target.value)}
          required
        />

        <button className="primary-btn" disabled={loading}>
          {loading ? "Searching..." : "Track"}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {result && (
        <div className="panel track-result">
          <h3>{result.subject}</h3>

          <p>
            <b>Reference:</b> {result.reference_number}
          </p>

          <p>
            <b>District:</b> {result.district}
          </p>

          <p>
            <b>Category:</b> {result.category}
          </p>

          <p>
            <b>Status:</b> <Status value={result.status} />
          </p>

          <p>{result.description}</p>

          <h4>Public status history</h4>

          {(result.history || []).map((history) => (
            <div className="history-item" key={history.id}>
              <b>{history.new_status}</b>
              {" · "}
              {new Date(history.created_at).toLocaleString()}

              <p>{history.remarks}</p>
            </div>
          ))}

          {(result.attachments || []).length > 0 && (
            <>
              <h4>Attachments</h4>

              {result.attachments.map((attachment) => (
                <p key={attachment.id}>
                  <a
                    href={attachment.file}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {attachment.original_name || "View attachment"}
                  </a>
                </p>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}

/* -------------------- CMO DASHBOARD -------------------- */

function CMODashboard() {
  const [items, setItems] = useState([]);
  const [stats, setStats] = useState({});
  const [reports, setReports] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function load() {
    setLoading(true);

    try {
      const [list, summary, actionReports] = await Promise.all([
        api.get("/grievances/cmo/list/"),
        api.get("/grievances/cmo/stats/"),
        api.get("/grievances/cmo/action-reports/"),
      ]);

      setItems(
        Array.isArray(list.data)
          ? list.data
          : list.data.results || []
      );

      setStats(summary.data);

      setReports(
        Array.isArray(actionReports.data)
          ? actionReports.data
          : actionReports.data.results || []
      );

      setError("");
    } catch (err) {
      setError(
        "Unable to load CMO data. Check your login, backend and API routes."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function analyze(reference) {
    try {
      await api.post(
        `/ai/analyze/${encodeURIComponent(reference)}/`
      );

      alert("AI analysis completed. Refreshing grievance list.");
      load();
    } catch (err) {
      alert(
        err.response?.data?.detail || "AI analysis failed."
      );
    }
  }

  async function reviewAI(reference, approved) {
    try {
      await api.post(
        `/ai/review/${encodeURIComponent(reference)}/`,
        { approved }
      );

      alert(
        approved
          ? "AI recommendations approved."
          : "AI recommendations rejected."
      );

      load();
    } catch (err) {
      alert(
        err.response?.data?.detail || "AI review failed."
      );
    }
  }

  async function assignGrievance(item) {
    const departmentId = window.prompt(
      "Enter the department ID:"
    );

    if (departmentId === null || !departmentId.trim()) return;

    const officerId = window.prompt(
      "Enter the officer user ID:"
    );

    if (officerId === null || !officerId.trim()) return;

    const remarks =
      window.prompt("Enter assignment remarks (optional):") || "";

    try {
      await api.post(
        `/grievances/cmo/${encodeURIComponent(item.reference_number)}/assign/`,
        {
          department_id: Number(departmentId),
          officer_id: Number(officerId),
          remarks,
        }
      );

      alert("Grievance assignment submitted.");
      load();
    } catch (err) {
      alert(
        JSON.stringify(
          err.response?.data || "Assignment failed."
        )
      );
    }
  }

  async function reviewActionReport(reportId, approved) {
    const remarks =
      window.prompt(
        approved
          ? "Enter approval remarks (optional):"
          : "Enter reason for rejection:"
      ) || "";

    try {
      await api.post(
        `/grievances/cmo/action-reports/${reportId}/review/`,
        {
          approved,
          remarks,
        }
      );

      alert(
        approved
          ? "Action report approved."
          : "Action report rejected. Grievance returned for further action."
      );

      load();
    } catch (err) {
      alert(
        JSON.stringify(
          err.response?.data || "Action report review failed."
        )
      );
    }
  }

  return (
    <DashboardLayout
      title="CMO Dashboard"
      subtitle="Monitor grievances, assignments and AI-assisted recommendations."
    >
      <div className="stats-grid">
        <Stat
          title="Total"
          value={stats.total ?? items.length}
          icon={<ClipboardList />}
        />

        <Stat
          title="Pending"
          value={stats.pending ?? "—"}
          icon={<RefreshCw />}
        />

        <Stat
          title="Resolved"
          value={stats.resolved ?? "—"}
          icon={<CheckCircle />}
        />

        <Stat
          title="Overdue"
          value={stats.overdue ?? "—"}
          icon={<AlertCircle />}
        />
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* ALL GRIEVANCES */}

      <div className="panel">
        <div className="panel-heading">
          <h3>All Grievances</h3>

          <button
            className="outline-btn small-btn"
            onClick={load}
            disabled={loading}
          >
            {loading ? "Loading..." : "Refresh"}
          </button>
        </div>

        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                <th>Reference</th>
                <th>Citizen</th>
                <th>District</th>
                <th>Category</th>
                <th>Priority</th>
                <th>Status</th>
                <th>AI Assistant</th>
                <th>Assignment</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>
                    <b>{item.reference_number}</b>
                    <small>{item.subject}</small>
                  </td>

                  <td>{item.citizen_name || "Citizen"}</td>
                  <td>{item.district}</td>
                  <td>{item.category}</td>
                  <td>{item.priority}</td>

                  <td>
                    <Status value={item.status} />
                  </td>

                  <td className="ai-actions">
                    {!item.ai_summary ? (
                      <button
                        className="primary-btn tiny-btn"
                        onClick={() =>
                          analyze(item.reference_number)
                        }
                      >
                        Analyze
                      </button>
                    ) : (
                      <>
                        <small>
                          {item.ai_suggested_department ||
                            "Department not identified"}
                          <br />
                          {item.ai_suggested_category} ·{" "}
                          {item.ai_suggested_priority}
                        </small>

                        <button
                          className="primary-btn tiny-btn"
                          onClick={() =>
                            reviewAI(item.reference_number, true)
                          }
                        >
                          Approve
                        </button>

                        <button
                          className="outline-btn tiny-btn"
                          onClick={() =>
                            reviewAI(item.reference_number, false)
                          }
                        >
                          Reject
                        </button>
                      </>
                    )}
                  </td>

                  <td>
                    <small>
                      {item.department_name || "Not assigned"}
                      <br />
                      {item.officer_name || ""}
                    </small>

                    <button
                      className="outline-btn tiny-btn"
                      onClick={() => assignGrievance(item)}
                    >
                      Assign
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {items.length === 0 && (
          <p className="empty-state">No grievances found.</p>
        )}
      </div>

      {/* OFFICER ACTION REPORTS */}

      <div className="panel">
        <div className="panel-heading">
          <h3>Officer Action Reports</h3>

          <button
            className="outline-btn small-btn"
            onClick={load}
            disabled={loading}
          >
            Refresh Reports
          </button>
        </div>

        {reports.length === 0 ? (
          <p className="empty-state">
            No action reports have been submitted yet.
          </p>
        ) : (
          reports.map((report) => (
            <div className="history-item" key={report.id}>
              <h4>Action Report #{report.id}</h4>

              <p>
                <b>Grievance ID:</b> {report.grievance}
              </p>

              <p>
                <b>Officer:</b> {report.officer}
              </p>

              <p>
                <b>Submission date:</b>{" "}
                {report.submitted_at
                  ? new Date(report.submitted_at).toLocaleString()
                  : "—"}
              </p>

              <p>
                <b>Submitted to CMO:</b>{" "}
                {report.submitted_to_cmo ? "Yes" : "No"}
              </p>

              {report.investigation_details && (
                <p>
                  <b>Investigation:</b>{" "}
                  {report.investigation_details}
                </p>
              )}

              {report.action_taken && (
                <p>
                  <b>Action taken:</b> {report.action_taken}
                </p>
              )}

              {report.resolution_details && (
                <p>
                  <b>Resolution details:</b>{" "}
                  {report.resolution_details}
                </p>
              )}

              {report.submitted_to_cmo && (
                <div className="hero-actions">
                  <button
                    className="primary-btn tiny-btn"
                    onClick={() =>
                      reviewActionReport(report.id, true)
                    }
                  >
                    Approve Report
                  </button>

                  <button
                    className="outline-btn tiny-btn"
                    onClick={() =>
                      reviewActionReport(report.id, false)
                    }
                  >
                    Reject Report
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </DashboardLayout>
  );
}

/* -------------------- OFFICER DASHBOARD -------------------- */

function OfficerDashboard() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function load() {
    setLoading(true);

    try {
      const response = await api.get("/grievances/officer/list/");

      setItems(
        Array.isArray(response.data)
          ? response.data
          : response.data.results || []
      );

      setError("");
    } catch {
      setError("Unable to load assigned grievances.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function updateStatus(reference, status) {
    const remarks = window.prompt("Enter your remarks:");

    if (remarks === null) return;

    try {
      await api.patch(
        `/grievances/officer/${encodeURIComponent(reference)}/status/`,
        { status, remarks }
      );

      alert("Status updated.");
      load();
    } catch (err) {
      alert(
        JSON.stringify(
          err.response?.data || "Status update failed."
        )
      );
    }
  }

  async function submitReport(reference) {
    const investigation_details = window.prompt(
      "Investigation details:"
    );

    if (!investigation_details?.trim()) return;

    const action_taken = window.prompt("Action taken:");

    if (!action_taken?.trim()) return;

    const resolution_details = window.prompt(
      "Resolution details:"
    );

    if (resolution_details === null) return;

    try {
      await api.post(
        `/grievances/officer/${encodeURIComponent(reference)}/action-report/`,
        {
          investigation_details,
          action_taken,
          resolution_details,
        }
      );

      alert("Action report submitted to CMO.");
      load();
    } catch (err) {
      alert(
        JSON.stringify(
          err.response?.data || "Report submission failed."
        )
      );
    }
  }

  return (
    <DashboardLayout
      title="Officer Dashboard"
      subtitle="Review and act on grievances assigned to you."
    >
      {error && <div className="error-message">{error}</div>}

      <div className="panel">
        <div className="panel-heading">
          <h3>Assigned Grievances</h3>

          <button
            className="outline-btn small-btn"
            onClick={load}
            disabled={loading}
          >
            {loading ? "Loading..." : "Refresh"}
          </button>
        </div>

        <GrievanceTable items={items} />

        {items.map((item) => (
          <div className="officer-actions" key={item.id}>
            <div>
              <b>{item.reference_number}</b>
              <small>{item.subject}</small>
            </div>

            <button
              className="outline-btn tiny-btn"
              onClick={() =>
                updateStatus(
                  item.reference_number,
                  "UNDER_REVIEW"
                )
              }
            >
              Under Review
            </button>

            <button
              className="outline-btn tiny-btn"
              onClick={() =>
                updateStatus(
                  item.reference_number,
                  "IN_PROGRESS"
                )
              }
            >
              In Progress
            </button>

            <button
              className="primary-btn tiny-btn"
              onClick={() =>
                submitReport(item.reference_number)
              }
            >
              Submit Action Report
            </button>
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
}

/* -------------------- SHARED COMPONENTS -------------------- */

function DashboardLayout({ title, subtitle, children }) {
  return (
    <main className="dashboard-wrap">
      <div className="dashboard-heading">
        <div>
          <span className="eyebrow">CM KERALA PORTAL</span>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
      </div>

      {children}
    </main>
  );
}

function Stat({ title, value, icon }) {
  return (
    <div className="stat-card">
      <div>
        <span>{title}</span>
        <strong>{value}</strong>
      </div>

      <div className="stat-icon">{icon}</div>
    </div>
  );
}

function Status({ value }) {
  const label = (value || "").replaceAll("_", " ");

  return (
    <span
      className={`status status-${(value || "").toLowerCase()}`}
    >
      {label}
    </span>
  );
}

function GrievanceTable({ items }) {
  if (!items.length) {
    return <p className="empty-state">No grievances found.</p>;
  }

  return (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Reference</th>
            <th>District</th>
            <th>Category</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>
                <b>{item.reference_number}</b>
                <small>{item.subject}</small>
              </td>

              <td>{item.district}</td>
              <td>{item.category}</td>
              <td>{item.priority}</td>

              <td>
                <Status value={item.status} />
              </td>

              <td>
                {item.created_at
                  ? new Date(item.created_at).toLocaleDateString()
                  : "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/* -------------------- APP ROUTES -------------------- */

function AppShell() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/about" element={<About />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
        <Route path="/departments" element={<Departments />} />
        <Route path="/faq" element={<FAQ />} />

        <Route path="/login" element={<AuthPage />} />
        <Route
          path="/register"
          element={<AuthPage register />}
        />

        <Route path="/track" element={<TrackGrievance />} />
        <Route path="/contact" element={<Contact />} />

        <Route
          path="/citizen"
          element={
            <Protected roles={["CITIZEN"]}>
              <CitizenDashboard />
            </Protected>
          }
        />

        <Route
          path="/submit"
          element={
            <Protected roles={["CITIZEN"]}>
              <SubmitGrievance />
            </Protected>
          }
        />

        <Route
          path="/cmo"
          element={
            <Protected roles={["CMO_ADMIN"]}>
              <CMODashboard />
            </Protected>
          }
        />

        <Route
          path="/officer"
          element={
            <Protected roles={["OFFICER"]}>
              <OfficerDashboard />
            </Protected>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppShell />
    </BrowserRouter>
  );
}
