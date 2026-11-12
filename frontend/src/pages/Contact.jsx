
import { useState } from "react";
import api from "../services/api";

export default function Contact() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccess("");
    setError("");

    try {
      await api.post("/contact/", form);
      setSuccess("Your enquiry has been submitted successfully!");
      setForm({
        name: "",
        email: "",
        subject: "",
        message: "",
      });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to submit your enquiry. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-12">
      <div className="mx-auto max-w-3xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-slate-900">
            Contact Us
          </h1>
          <p className="mt-3 text-slate-600">
            Have a question? Send your enquiry to our support team.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-5 rounded-xl bg-white p-8 shadow"
        >
          {success && (
            <div className="rounded-lg bg-green-100 p-3 text-green-800">
              {success}
            </div>
          )}

          {error && (
            <div className="rounded-lg bg-red-100 p-3 text-red-700">
              {error}
            </div>
          )}

          <div>
            <label className="mb-2 block font-medium">Full Name</label>
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              required
              maxLength={150}
              className="w-full rounded-lg border p-3 outline-none focus:border-blue-600"
              placeholder="Enter your name"
            />
          </div>

          <div>
            <label className="mb-2 block font-medium">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
              className="w-full rounded-lg border p-3 outline-none focus:border-blue-600"
              placeholder="Enter your email"
            />
          </div>

          <div>
            <label className="mb-2 block font-medium">Subject</label>
            <input
              name="subject"
              value={form.subject}
              onChange={handleChange}
              required
              maxLength={200}
              className="w-full rounded-lg border p-3 outline-none focus:border-blue-600"
              placeholder="Enter subject"
            />
          </div>

          <div>
            <label className="mb-2 block font-medium">Message</label>
            <textarea
              name="message"
              value={form.message}
              onChange={handleChange}
              required
              rows={5}
              className="w-full rounded-lg border p-3 outline-none focus:border-blue-600"
              placeholder="Write your enquiry..."
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-700 px-6 py-3 font-semibold text-white hover:bg-blue-800 disabled:opacity-60"
          >
            {loading ? "Submitting..." : "Submit Enquiry"}
          </button>
        </form>
      </div>
    </div>
  );
}
