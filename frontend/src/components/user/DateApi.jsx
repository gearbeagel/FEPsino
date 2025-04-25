import { format, formatDistanceToNow, parse } from "date-fns";

export default function DisplayDate({ dateString }) {
    // Parse the date string into a valid Date object
    const date = parse(dateString, "dd-MM-yyyy HH:mm:ss", new Date());
    const relativeTime = formatDistanceToNow(date, { addSuffix: true });

    return (
        <div>
            <span>{relativeTime}</span>
        </div>
    );
}